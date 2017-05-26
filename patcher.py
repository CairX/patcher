import os
import shutil
import sys


VERSIONS_LOCATION = "versions"
INSTALL_LOCATION = "install"
VERSION_FILE = os.path.join(INSTALL_LOCATION, "version.txt")


def update():
	current = 0
	with open(VERSION_FILE) as file:
		current = file.readline().strip()
	print(current)
	versions = sorted(os.listdir("versions"))
	print(versions)
	print(versions.index(current))
	print(versions[versions.index(current) + 1:])

	for version in versions[versions.index(current) + 1:]:
		patch(version)


def patch(version):
	version_path = os.path.join(VERSIONS_LOCATION, version)
	version_changes = os.path.join(version_path, "changes.txt")

	with open(version_changes) as changes:
		for change in changes:
			values = change.split(" ", maxsplit=1)
			action = values[0]
			path = values[1].strip()
			dst = os.path.join(INSTALL_LOCATION, path)

			if action == "++":
				shutil.copyfile(os.path.join(version_path, path), dst)
			elif action == "--":
				os.remove(dst)
			else:
				continue

	with open(VERSION_FILE, "w") as file:
		file.write(version)


def restore():
	shutil.rmtree(INSTALL_LOCATION)
	os.makedirs(INSTALL_LOCATION)
	patch("1")


if __name__ == "__main__":
	if len(sys.argv) == 1:
		update()
	elif sys.argv[1] == "restore":
		restore()
