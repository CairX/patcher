import os
import shutil

with open("versions/2/changes.txt") as changes:
	for change in changes:
		values = change.split(" ", maxsplit=1)
		action = values[0]
		path = values[1].strip()

		if action == "++":
			shutil.copyfile("versions/2/" + path, "install/" + path)
		elif action == "--":
			os.remove("install/" + path)
		else:
			continue
