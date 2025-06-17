import os
import json
import base64
import getpass
import argparse
import shutil
import sys
from pathlib import Path
import importlib.util
from Crypto.Cipher import AES
from argon2.low_level import hash_secret_raw, Type
from concurrent.futures import ThreadPoolExecutor
import tempfile
import subprocess

try:
    from mockbit.ransom_sim import restore_simulation as _restore_sim
except Exception:  # pragma: no cover - optional module for binaries
    try:
        mod_path = Path(__file__).with_name("mockbit") / "ransom_sim.py"
        spec = importlib.util.spec_from_file_location("mockbit.ransom_sim", mod_path)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            _restore_sim = mod.restore_simulation
        else:
            _restore_sim = None
    except Exception:
        _restore_sim = None

if _restore_sim is None:
    def _restore_sim(target_dir: Path, threads: int = 8) -> None:
        """Fallback restore if module import fails."""
        _KEY = 0xAA

        def _xor_bytes(data: bytes) -> bytes:
            return bytes(b ^ _KEY for b in data)

        def _process_file(file_path: Path) -> None:
            if not file_path.name.endswith(".mocklock"):
                return
            try:
                with open(file_path, "rb") as f:
                    data = f.read()
                dec = _xor_bytes(data)
                tmp_fd, tmp_name = tempfile.mkstemp(dir=str(file_path.parent))
                with os.fdopen(tmp_fd, "wb") as tmp:
                    tmp.write(dec)
                    tmp.flush()
                    os.fsync(tmp.fileno())
                out = file_path.with_suffix("")
                os.replace(tmp_name, out)
                os.unlink(file_path)
            except Exception:
                pass

        with ThreadPoolExecutor(max_workers=threads) as exe:
            for dirpath, _, files in os.walk(target_dir):
                root = Path(dirpath)
                for name in files:
                    fp = root / name
                    if not fp.is_file() or fp.is_symlink():
                        continue
                    if not fp.name.endswith(".mocklock"):
                        continue
                    exe.submit(_process_file, fp)
                note = root / "README_MOCKBIT_RESTORE.txt"
                try:
                    note.unlink()
                except Exception:
                    pass

# Default options
START_PATH = "folder"
KEY_FILENAME = "MOCKBIT_KEY.txt"
NONCE_SIZE = 12  # Muss identisch zum Wert in encrypt_all.py sein
ARGON2_TIME = 2
ARGON2_MEMORY = 102400
ARGON2_PARALLELISM = 8


def parse_args():
    parser = argparse.ArgumentParser(
        description="Decrypt all .mock files in a folder recursively"
    )
    parser.add_argument(
        "--path",
        default=START_PATH,
        help="Target directory (default: %(default)s)",
    )
    parser.add_argument(
        "--ransom-sim",
        action="store_true",
        help="Restore files created by the ransomware simulation",
    )
    parser.add_argument(
        "--sim-path",
        default=os.path.join(os.getcwd(), "testdata"),
        help="Directory for ransomware simulation",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force simulation on large directories",
    )
    parser.add_argument("--time", type=int, help="Override Argon2 time cost")
    parser.add_argument("--memory", type=int, help="Override Argon2 memory cost")
    parser.add_argument(
        "--parallelism", type=int, help="Override Argon2 degree of parallelism"
    )
    return parser.parse_args()

def decrypt_file(file_path, key):
    try:
        if os.path.getsize(file_path) < NONCE_SIZE + 16:
            print("Überspringe zu kleine Datei:", file_path)
            return
        with open(file_path, "rb") as f:
            nonce = f.read(NONCE_SIZE)
            tag = f.read(16)
            ct = f.read()
        if len(nonce) != NONCE_SIZE:
            print("Ungültiger Nonce in Datei:", file_path)
            return
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        try:
            data = cipher.decrypt_and_verify(ct, tag)
        except ValueError:
            print("Authentifizierung fehlgeschlagen für:", file_path)
            return

        # Hier wird .mock sauber entfernt:
        base, ext = os.path.splitext(file_path)
        if ext == ".mock":
            out_path = base
        else:
            out_path = file_path + ".decrypted"

        with open(out_path, "wb") as f:
            f.write(data)
        print("Entschlüsselt:", file_path, "->", out_path)
        os.remove(file_path)  # Die .mock-Datei wird nach erfolgreichem Entschlüsseln gelöscht!
    except Exception as e:
        print(f"Fehler beim Entschlüsseln von {file_path}: {e}")

def find_and_decrypt_all_files(path, key):
    for dirpath, _, files in os.walk(path):
        for name in files:
            if name.endswith(".mock"):
                file_path = os.path.join(dirpath, name)
                decrypt_file(file_path, key)

if __name__ == "__main__":
    args = parse_args()

    if args.ransom_sim:
        sim_dir = Path(args.sim_path)
        if str(sim_dir) in ["/", "/home", "/var", "/etc"]:
            print("Refusing to run ransomware simulation on system directories.")
            sys.exit(1)
        if shutil.disk_usage(sim_dir).free < 10 * 1024 * 1024:
            print("Not enough free space for simulation.")
            sys.exit(1)
        file_count = sum(len(files) for _, _, files in os.walk(sim_dir))
        if file_count > 10000 and not args.force:
            print(f"{file_count} files detected. Re-run with --force to continue.")
            sys.exit(1)
        if _restore_sim is None:
            print("Ransom simulation module unavailable.")
            sys.exit(1)

        print("\033[91m⚠️  Ransom-Sim restore mode active – EDR alarms expected.\033[0m")
        _restore_sim(sim_dir)
        sys.exit(0)

    key_path = os.path.join(args.path, KEY_FILENAME)
    if not os.path.exists(key_path):
        print("Key-Datei nicht gefunden:", key_path)
        sys.exit(1)

    with open(key_path, "r") as f:
        info = json.load(f)
    try:
        salt = base64.b64decode(info["salt"])
        time_cost = int(info.get("time", ARGON2_TIME))
        mem_cost = int(info.get("memory", ARGON2_MEMORY))
        parallel = int(info.get("parallelism", ARGON2_PARALLELISM))
    except Exception as e:
        print("Key-Datei ungültig:", e)
        sys.exit(1)

    if args.time is not None:
        time_cost = args.time
    if args.memory is not None:
        mem_cost = args.memory
    if args.parallelism is not None:
        parallel = args.parallelism

    passphrase = getpass.getpass("Bitte Passphrase zum Entschlüsseln eingeben:\n")
    key = hash_secret_raw(
        secret=passphrase.encode(),
        salt=salt,
        time_cost=time_cost,
        memory_cost=mem_cost,
        parallelism=parallel,
        hash_len=32,
        type=Type.ID,
    )

    print(f"Starte Entschlüsselung in: {args.path}")
    find_and_decrypt_all_files(args.path, key)
    print("Fertig.")
