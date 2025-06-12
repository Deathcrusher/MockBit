import os
import base64
from Crypto.Cipher import AES

# Zielordner anpassen!
START_PATH = "/aim"

def unpad(data):
    pad_length = data[-1]
    return data[:-pad_length]

def decrypt_file(file_path, key):
    try:
        if os.path.getsize(file_path) < 17:
            print("Überspringe zu kleine Datei:", file_path)
            return
        with open(file_path, "rb") as f:
            iv = f.read(16)
            ct = f.read()
        if len(iv) != 16:
            print("Ungültiger IV in Datei:", file_path)
            return
        cipher = AES.new(key, AES.MODE_CBC, iv)
        data = cipher.decrypt(ct)
        data = unpad(data)
        out_path = file_path[:-4] if file_path.endswith(".enc") else file_path + ".decrypted"
        with open(out_path, "wb") as f:
            f.write(data)
        print("Entschlüsselt:", file_path, "->", out_path)
        os.remove(file_path)  # Die .enc-Datei wird nach erfolgreichem Entschlüsseln gelöscht!
    except Exception as e:
        print(f"Fehler beim Entschlüsseln von {file_path}: {e}")

def find_and_decrypt_all_files(path, key):
    for dirpath, _, files in os.walk(path):
        for name in files:
            if name.endswith(".enc"):
                file_path = os.path.join(dirpath, name)
                decrypt_file(file_path, key)

if __name__ == "__main__":
    key_b64 = input("Bitte gib den Schlüssel (BASE64) zum Entschlüsseln ein:\n").strip()
    try:
        key = base64.b64decode(key_b64)
        if len(key) != 32:
            raise ValueError("Falsche Schlüssellänge!")
    except Exception as e:
        print("Ungültiger Schlüssel! Fehler:", e)
        exit(1)
    print(f"Starte Entschlüsselung in: {START_PATH}")
    find_and_decrypt_all_files(START_PATH, key)
    print("Fertig.")
