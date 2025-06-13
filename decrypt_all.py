import os
import json
import base64
import getpass
from Crypto.Cipher import AES
from argon2.low_level import hash_secret_raw, Type

# Zielordner anpassen!
START_PATH = "folder"
KEY_FILENAME = "MOCKBIT_KEY.txt"
NONCE_SIZE = 12  # Muss identisch zum Wert in encrypt_all.py sein
ARGON2_TIME = 2
ARGON2_MEMORY = 102400
ARGON2_PARALLELISM = 8

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
        time_cost = int(info.get("time", ARGON2_TIME))
        mem_cost = int(info.get("memory", ARGON2_MEMORY))
        parallel = int(info.get("parallelism", ARGON2_PARALLELISM))
    except Exception as e:
        print("Key-Datei ungültig:", e)
        exit(1)

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

    print(f"Starte Entschlüsselung in: {START_PATH}")
    find_and_decrypt_all_files(START_PATH, key)
    print("Fertig.")
