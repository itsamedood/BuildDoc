MAIN:=src/main.py
FLAGS:=-B
ARGS=-d -vb
EXPORT=export.py

debug:
	python3 $(FLAGS) $(MAIN) $(ARGS)

compile:
	python3 $(FLAGS) $(EXPORT)

package:
	python3 $(FLAGS) $(EXPORT) --zip
