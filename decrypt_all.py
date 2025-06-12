import os
import base64
from Crypto.Cipher import AES

# Verzeichnis anpassen!
START_PATH = "/pfad/zum/verzeichnis"
# Schlüssel aus dem Verschlüsselungsvorgang (BASE64-String) hier einfügen:
KEY_B64 = "HIER_DEIN_B64_KEY_EINFÜGEN"

def unpad(data):
    pad_length = data[-1]
    return data[:-pad_length]

def decrypt_file(file_path, key):
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
    with open(file_path.replace(".enc", ""), "wb") as f:
        f.write(unpad(data))
    os.remove(file_path)

def find_and_decrypt_all_files(path, key):
    for dirpath, _, files in os.walk(path):
        for name in files:
            if name.endswith(".enc"):
                file_path = os.path.join(dirpath, name)
                try:
                    decrypt_file(file_path, key)
                    print("Entschlüsselt:", file_path)
                except Exception as e:
                    print("Fehler bei", file_path, e)

if __name__ == "__main__":
    key = base64.b64decode(KEY_B64)
    find_and_decrypt_all_files(START_PATH, key)
    print("Fertig.")
