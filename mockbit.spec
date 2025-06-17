# PyInstaller spec including ransomware simulator
block_cipher = None

a = Analysis(['encrypt_all.py', 'decrypt_all.py'],
             hiddenimports=['mockbit.ransom_sim', 'Crypto', 'Crypto.Random',
                            'Crypto.Cipher', 'argon2'],
             )
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz, a.scripts[0], name='encrypt', onefile=True)
exe2 = EXE(pyz, a.scripts[1], name='decrypt', onefile=True)
