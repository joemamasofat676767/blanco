from pathlib import Path
import sys

ROOT = Path(__file__).parent.parent

sys.path.insert(0, f"{str(ROOT)}/main")

import main as SnS
print(SnS.generate("obama"))

PROTECTED_FILES = list(ROOT.glob("*/main.*"))
command = input(" >> ")

generate("obama")

while command != "q":
	if command.startswith("c "):
		target = command[2:]
		file = list(ROOT.glob(f"*/{target}"))

		if not file or not file[0].is_file():
			print(f" > no file: {target}")
		elif file[0] in PROTECTED_FILES:
			print(f" > file protected: {target}")
		else:
			file[0].write_text("")
			print(f" > file cleared: {target}")
	elif command.startswith("g "):
		StartText = command[2:]
		print(f"generated: {main.generate()}")
	elif command == "q":
		break
	else:
		print(f" > invalid command: {command}")

	command = input(" >> ")