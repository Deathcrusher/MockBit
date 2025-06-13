import os
import json
import base64
import getpass
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

# Zielordner anpassen!
START_PATH = "folder"
KEY_FILENAME = "MOCKBIT_KEY.txt"
NONCE_SIZE = 12  # Muss identisch zum Wert in encrypt_all.py sein
PBKDF2_ITERATIONS = 200_000



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
    key_path = os.path.join(START_PATH, KEY_FILENAME)
    if not os.path.exists(key_path):
        print("Key-Datei nicht gefunden:", key_path)
        exit(1)

    with open(key_path, "r") as f:
        info = json.load(f)
    try:
        salt = base64.b64decode(info["salt"])
        iterations = int(info.get("iterations", PBKDF2_ITERATIONS))
    except Exception as e:
        print("Key-Datei ungültig:", e)
        exit(1)

    passphrase = getpass.getpass("Bitte Passphrase zum Entschlüsseln eingeben:\n")
    key = PBKDF2(passphrase, salt, dkLen=32, count=iterations)

    print(f"Starte Entschlüsselung in: {START_PATH}")
    find_and_decrypt_all_files(START_PATH, key)
    print("Fertig.")
