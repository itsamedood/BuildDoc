MAIN	:=	src/main.py
BINARY	:=	build
VERSION := 0.0.1

OS		:=	$(shell uname -s | tr A-Z a-z)
SYS		:=
ZIP		:=
OUTPATH :=

# Checking the OS.
ifeq ($(OS), linux)
	SYS := linux
else ifeq ($(OS), darwin)
	SYS := macos
else
	SYS := windows
endif

# Updating paths.
OUTPATH  := bin/$(SYS)
ZIP		 := release/$(VERSION)/builddoc-$(SYS).zip

.PHONY: all
compile:
	@echo 🛠 Compiling... 🛠
	@echo -----------------
	cxfreeze --target-dir ./bin/$(SYS) --target-name $(BINARY) ./$(MAIN)

run:
	@python3 -B ./$(MAIN)
