.PHONY: all clean

BIN_DIR=bin
ENCRYPT_OUT=$(BIN_DIR)/encrypt
DECRYPT_OUT=$(BIN_DIR)/decrypt

all: $(ENCRYPT_OUT) $(DECRYPT_OUT)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(ENCRYPT_OUT): encrypt_all.py | $(BIN_DIR)
	pyinstaller --onefile --distpath $(BIN_DIR) --name encrypt $<
	@rm -rf build encrypt.spec

$(DECRYPT_OUT): decrypt_all.py | $(BIN_DIR)
	pyinstaller --onefile --distpath $(BIN_DIR) --name decrypt $<
	@rm -rf build decrypt.spec

clean:
	rm -rf build *.spec $(BIN_DIR)
