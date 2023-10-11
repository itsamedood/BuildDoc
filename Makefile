MAIN:=src/main.py
FLAGS:=-B
ARGS=-d -vb
EXPORT=export.py

debug:
	@printf Debugging...\n\n
	@python3 $(FLAGS) $(MAIN) $(ARGS)

compile:
	@printf Compiling...\n\n
	@python3 $(FLAGS) $(EXPORT)

package:
	@printf Packaging...\n\n
	@python3 $(FLAGS) $(EXPORT) --zip
