# Simple AES File Encrypt/Decrypt Scripts

**Verschlüssle und entschlüssele alle Dateien in einem Ordner (inkl. Unterordner) mit AES-256-GCM.**

## Voraussetzungen

- Python 3.x
- [PyCryptodome](https://www.pycryptodome.org/) und [argon2-cffi](https://pypi.org/project/argon2-cffi/) installieren:
  ```
  pip3 install -r requirements.txt
  ```
### Kompilierte Version

- Installiere `pyinstaller` und die oben genannten Bibliotheken auf der Build-Maschine.
- Führe `./compile.sh` aus, um eigenständige Binaries zu erzeugen.
- Die entstandenen Dateien liegen anschließend im Verzeichnis `bin/` und lassen sich ohne weitere Python-Abhängigkeiten nutzen.

 

## Verwendung

### 1. Verschlüsseln

- Passe `START_PATH` in `encrypt_all.py` auf dein Zielverzeichnis an.
- Starte das Skript und gib eine Passphrase ein:
  ```
  python3 encrypt_all.py
  ```
- Die Passphrase wird mittels Argon2id in einen Schlüssel abgeleitet.
- Parameter wie Salz und Zeit- und Speicherkosten werden in `MOCKBIT_KEY.txt` gespeichert.
- Alle Dateien werden als `.mock` verschlüsselt, Originaldateien werden sicher gelöscht.

### 2. Entschlüsseln

- Passe `START_PATH` in `decrypt_all.py` auf das Verzeichnis mit den `.mock`-Dateien an.
- Stelle sicher, dass `MOCKBIT_KEY.txt` dort liegt und gib dieselbe Passphrase ein.
- Starte das Skript:
  ```
  python3 decrypt_all.py
  ```
- Die Dateien werden wiederhergestellt, `.mock`-Dateien werden gelöscht.

## Hinweise

- **Unbedingt zuerst in einer Testumgebung ausprobieren!**
- Ohne den Schlüssel kann niemand die Daten wiederherstellen.
- Das Skript überschreibt keine existierenden Dateien beim Entschlüsseln, sondern gibt ihnen wieder ihren Originalnamen.
- Für Backups oder produktiven Einsatz bitte weiterentwickeln!

## Haftungsausschluss

Benutzung auf eigene Gefahr. Für Datenverlust oder Missbrauch wird keine Haftung übernommen.
