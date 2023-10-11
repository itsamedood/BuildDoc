from os import name, system
from sys import argv, exit


MAIN = "src/main.py"
BINARY = "build"
VERSION = "0.0.1"

OS = name
SYS: str | None
ZIP = ''
OUTPATH = ''


match OS:
    case "posix": SYS = "macos"
    case "linux": SYS = "linux"
    case "nt": SYS = "windows"
    case _: SYS = None


if SYS is None: print("Unknown OS."); exit(0)

OUTPATH = "bin/%s" %SYS
ZIP = f"release/{VERSION}/builddoc-{SYS}.zip"


def compile():
    print("🛠 Compiling... 🛠\n-----------------")
    system(f"pyinstaller --onefile --distpath ./bin/{SYS} --name {BINARY} ./{MAIN}")
    print("🛠️ Finished compiling! 🛠️\n------------------------")

def package():
    print("📦 Packaging... 📦\n------------------")
    print("📦 Finished packaging! 📦\n-------------------------")

if __name__ == "__main__": package() if len(argv) > 1 and argv[1] == "--zip" else compile()
