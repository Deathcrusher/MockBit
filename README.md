# Simple AES File Encrypt/Decrypt Scripts

**Verschlüssle und entschlüssele alle Dateien in einem Ordner (inkl. Unterordner) mit AES-256-GCM.**

## Voraussetzungen

- Python 3.x
- [PyCryptodome](https://www.pycryptodome.org/) installieren:
  ```
  pip3 install pycryptodome
  ```

## Verwendung

### 1. Verschlüsseln

- Passe `START_PATH` in `encrypt_all.py` auf dein Zielverzeichnis an.
- Starte das Skript:
  ```
  python3 encrypt_all.py
  ```
- Der erzeugte BASE64-Schlüssel wird angezeigt – **unbedingt sichern!**
- Alle Dateien werden als `.mock` verschlüsselt, Originaldateien werden gelöscht.

### 2. Entschlüsseln

- Passe `START_PATH` in `decrypt_all.py` auf das Verzeichnis mit den `.mock`-Dateien an.
- Trage den beim Verschlüsseln erhaltenen Schlüssel (BASE64) bei `KEY_B64` ein.
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
