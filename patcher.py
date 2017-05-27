import os
import shutil
import sys


VERSION_FILE = "version.txt"
CHANGES_FILE = "changes.txt"


def update(versions_path, install_path):
	current = 0
	with open(os.path.join(install_path, VERSION_FILE)) as file:
		current = file.readline().strip()

	versions = sorted(os.listdir("versions"))

	for version in versions[versions.index(current) + 1:]:
		patch(str(version), versions_path, install_path)


def patch(version, versions_path, install_path):
	print("Patch v." + str(version))

	version_path = os.path.join(versions_path, str(version))
	version_changes = os.path.join(version_path, CHANGES_FILE)

	with open(version_changes) as changes:
		for change in changes:
			values = change.split(" ", maxsplit=1)
			action = values[0]
			argument = values[1].strip()

			if action == "++":
				add(argument, version_path, install_path)
			elif action == "--":
				remove(argument, install_path)
			elif action == ">>":
				move(argument, install_path)
			else:
				continue

	with open(os.path.join(install_path, VERSION_FILE), "w") as file:
		file.write(version)


def add(entry, version_path, install_path):
	src = os.path.join(version_path, entry)
	dst = os.path.join(install_path, entry)
	shutil.copyfile(src, dst)
	print("++ " + dst)


def remove(entry, install_path):
	dst = os.path.join(install_path, entry)
	os.remove(dst)
	print("-- " + dst)


def move(argument, install_path):
	paths = argument.split(" ", maxsplit=1)
	src = os.path.join(install_path, paths[0])
	dst = os.path.join(install_path, paths[1])
	dstfolder = os.path.dirname(dst)

	if not os.path.exists(dstfolder):
		os.makedirs(dstfolder)

	shutil.move(src, dst)
	print(">> " + src + " to " + dst)


def install(version, versions_path, install_path):
	print("Install v." + str(version))
	version_path = os.path.join(versions_path, str(version))
	shutil.copytree(version_path, install_path)
	os.remove(os.path.join(install_path, CHANGES_FILE))

	with open(os.path.join(install_path, VERSION_FILE), "w") as file:
		file.write(str(version))


def uninstall(install_path):
	print("Uninstall")
	shutil.rmtree(install_path)


def restore(version, versions_path, install_path):
	uninstall(install_path)
	install(version, versions_path, install_path)


if __name__ == "__main__":
	VERSIONS_LOCATION = "versions"
	INSTALL_LOCATION = "install"

	if len(sys.argv) > 1:
		command =sys.argv[1]
		if command == "install":
			if len(sys.argv) >= 3:
				install(sys.argv[2], VERSIONS_LOCATION, INSTALL_LOCATION)
			else:
				install("1", VERSIONS_LOCATION, INSTALL_LOCATION)
		elif command == "uninstall":
			uninstall(INSTALL_LOCATION)
		elif command == "restore":
			if len(sys.argv) >= 3:
				restore(sys.argv[2], VERSIONS_LOCATION, INSTALL_LOCATION)
			else:
				restore("1", VERSIONS_LOCATION, INSTALL_LOCATION)
	else:
		update(VERSIONS_LOCATION, INSTALL_LOCATION)
	print("Done")
