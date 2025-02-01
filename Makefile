# Haha Makefile in a project made to replace it.

EXEC=build
CC=gcc
SRC=$(wildcard src/*.c)
OBJ=$(patsubst src/%.c, obj/%.o, $(SRC))
INCLUDES=-Iinclude -I/usr/include -I/usr/local/include
CFLAGS=-Wall -Werror -std=c99 $(INCLUDES)

.PHONY: all clean
all: $(EXEC)

$(EXEC): $(OBJ)
	$(CC) $(OBJ) $(LDFLAGS) -o bin/$(EXEC)

obj/%.o: src/%.c | obj
	$(CC) $(CFLAGS) -c $< -o $@

obj:
	mkdir -p obj bin

clean:
	rm -rf obj bin
