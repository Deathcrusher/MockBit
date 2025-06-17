.PHONY: all clean

BIN_DIR=bin
ENCRYPT_OUT=$(BIN_DIR)/encrypt
DECRYPT_OUT=$(BIN_DIR)/decrypt
PYI_OPTS=--onefile --distpath $(BIN_DIR) \
        --hidden-import=Crypto --hidden-import=Crypto.Random \
        --hidden-import=Crypto.Cipher --hidden-import=argon2 \
        --hidden-import=mockbit.ransom_sim

all: $(ENCRYPT_OUT) $(DECRYPT_OUT)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(ENCRYPT_OUT): encrypt_all.py | $(BIN_DIR)
	pyinstaller $(PYI_OPTS) --name encrypt $<
	@rm -rf build encrypt.spec

$(DECRYPT_OUT): decrypt_all.py | $(BIN_DIR)
	pyinstaller $(PYI_OPTS) --name decrypt $<
	@rm -rf build decrypt.spec

clean:
	rm -rf build *.spec $(BIN_DIR)
