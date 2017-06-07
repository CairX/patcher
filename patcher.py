import logging
import os
import shutil
import sys


VERSION_FILE = "version.txt"
CHANGES_FILE = "changes.txt"


class Log(object):
	__levels = {}

	@classmethod
	def level(cls, level, value):
		cls.__levels[level] = value

	@classmethod
	def message(cls, level, message):
		if level in cls.__levels and cls.__levels[level]:
			print(message)


def update(versions_path, install_path):
	current = 0
	with open(os.path.join(install_path, VERSION_FILE)) as file:
		current = file.readline().strip()

	versions = sorted(os.listdir(versions_path))

	for version in versions[versions.index(current) + 1:]:
		patch(str(version), versions_path, install_path)


def patch(version, versions_path, install_path):
	Log.message("INFO", "Patch version " + str(version))

	version_path = os.path.join(versions_path, str(version))
	version_changes = os.path.join(version_path, CHANGES_FILE)

	with open(version_changes) as changes:
		for change in changes:
			change = change.strip()
			action = change[:2]
			argument = change[2:].strip()

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
	entry = entry.strip("\"")
	src = os.path.join(version_path, entry)

	if not os.path.exists(src):
		Log.message("WARNING", "\tSource file doesn't exist: " + src)
		return

	dst = os.path.join(install_path, entry)
	dstfolder = os.path.dirname(dst)

	if os.path.isfile(src):
		if not os.path.exists(dstfolder):
			os.makedirs(dstfolder)

		shutil.copyfile(src, dst)
	else:
		if os.path.exists(dst):
			shutil.rmtree(dst)

		shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".keep"))

	Log.message("DETAILS", "\t++ " + dst)


def remove(entry, install_path):
	entry = entry.strip("\"")
	dst = os.path.join(install_path, entry)

	if not os.path.exists(dst):
		Log.message("WARNING", "\tDestination file doesn't exist: " + dst)
		return

	if os.path.isfile(dst):
		os.remove(dst)
	else:
		shutil.rmtree(dst)

	Log.message("DETAILS", "\t-- " + dst)


def move(argument, install_path):
	paths = argument.split("\" \"", maxsplit=1)
	paths = [path.strip("\"") for path in paths]

	src = os.path.join(install_path, paths[0])
	dst = os.path.join(install_path, paths[1])

	if os.path.isfile(src):
		dst_directory = os.path.dirname(dst)
		if not os.path.exists(dst_directory):
			os.makedirs(dst_directory)

	if os.path.exists(dst):
		Log.message("WARNING", "\tDestination already exist: " + dst)

	shutil.move(src, dst)
	Log.message("DETAILS", "\t>> " + src + " to " + dst)


def install(version, versions_path, install_path):
	Log.message("INFO", "Install version " + str(version))
	version_path = os.path.join(versions_path, str(version))
	shutil.copytree(version_path, install_path, ignore=shutil.ignore_patterns(".keep"))
	os.remove(os.path.join(install_path, CHANGES_FILE))

	with open(os.path.join(install_path, VERSION_FILE), "w") as file:
		file.write(str(version))


def uninstall(install_path):
	Log.message("INFO", "Uninstall")
	shutil.rmtree(install_path)


def restore(version, versions_path, install_path):
	uninstall(install_path)
	install(version, versions_path, install_path)


if __name__ == "__main__":
	VERSIONS_LOCATION = "versions"
	INSTALL_LOCATION = "install"

	Log.level("INFO", False)
	Log.level("DETAILS", False)

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
