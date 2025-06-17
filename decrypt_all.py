import os
import json
import base64
import getpass
import argparse
import shutil
from pathlib import Path
from Crypto.Cipher import AES
from argon2.low_level import hash_secret_raw, Type

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
        help="Run ransomware simulation instead of decryption",
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
            exit(1)
        if shutil.disk_usage(sim_dir).free < 10 * 1024 * 1024:
            print("Not enough free space for simulation.")
            exit(1)
        file_count = sum(len(files) for _, _, files in os.walk(sim_dir))
        if file_count > 10000 and not args.force:
            print(f"{file_count} files detected. Re-run with --force to continue.")
            exit(1)
        from mockbit.ransom_sim import run_simulation

        print("\033[91m⚠️  Ransom-Sim mode active – EDR alarms expected.\033[0m")
        run_simulation(sim_dir)
        exit(0)

    key_path = os.path.join(args.path, KEY_FILENAME)
    if not os.path.exists(key_path):
        print("Key-Datei nicht gefunden:", key_path)
        exit(1)

    with open(key_path, "r") as f:
        info = json.load(f)
    try:
        salt = base64.b64decode(info["salt"])
        time_cost = int(info.get("time", ARGON2_TIME))
        mem_cost = int(info.get("memory", ARGON2_MEMORY))
        parallel = int(info.get("parallelism", ARGON2_PARALLELISM))
    except Exception as e:
        print("Key-Datei ungültig:", e)
        exit(1)

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
