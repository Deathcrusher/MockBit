import os
import json
import base64
import getpass
import argparse
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from argon2.low_level import hash_secret_raw, Type

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

if __name__ == "__main__":
    args = parse_args()

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
    print("Fertig.")
