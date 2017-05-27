import os
import shutil
import sys


VERSIONS_LOCATION = "versions"
INSTALL_LOCATION = "install"
VERSION_FILE = os.path.join(INSTALL_LOCATION, "version.txt")
CHANGES_FILE = "changes.txt"


def update():
	current = 0
	with open(VERSION_FILE) as file:
		current = file.readline().strip()

	versions = sorted(os.listdir("versions"))

	for version in versions[versions.index(current) + 1:]:
		patch(str(version))


def patch(version):
	print("Patch v." + str(version))

	version_path = os.path.join(VERSIONS_LOCATION, str(version))
	version_changes = os.path.join(version_path, CHANGES_FILE)

	with open(version_changes) as changes:
		for change in changes:
			values = change.split(" ", maxsplit=1)
			action = values[0]
			argument = values[1].strip()

			if action == "++":
				add(argument, version_path)
			elif action == "--":
				remove(argument)
			elif action == ">>":
				move(argument)
			else:
				continue

	with open(VERSION_FILE, "w") as file:
		file.write(version)


def add(path, version_path):
	dst = os.path.join(INSTALL_LOCATION, path)
	src = os.path.join(version_path, path)
	shutil.copyfile(src, dst)
	print("++ " + dst)


def remove(path):
	dst = os.path.join(INSTALL_LOCATION, path)
	os.remove(dst)
	print("-- " + dst)


def move(argument):
	paths = argument.split(" ", maxsplit=1)
	src = os.path.join(INSTALL_LOCATION, paths[0])
	dst = os.path.join(INSTALL_LOCATION, paths[1])
	dstfolder = os.path.dirname(dst)

	if not os.path.exists(dstfolder):
		os.makedirs(dstfolder)

	shutil.move(src, dst)
	print(">> " + src + " to " + dst)

def install(version=1):
	print("Install v." + str(version))
	version_path = os.path.join(VERSIONS_LOCATION, str(version))
	shutil.copytree(version_path, INSTALL_LOCATION)
	os.remove(os.path.join(INSTALL_LOCATION, CHANGES_FILE))

	with open(VERSION_FILE, "w") as file:
		file.write(str(version))


def uninstall():
	print("Uninstall")
	shutil.rmtree(INSTALL_LOCATION)


def restore(version=1):
	uninstall()
	install(version)


if __name__ == "__main__":
	if len(sys.argv) > 1:
		command =sys.argv[1]
		if command == "install":
			if len(sys.argv) >= 3:
				install(sys.argv[2])
			else:
				install()
		elif command == "uninstall":
			uninstall()
		elif command == "restore":
			if len(sys.argv) >= 3:
				restore(sys.argv[2])
			else:
				restore()
	else:
		update()
	print("Done")
