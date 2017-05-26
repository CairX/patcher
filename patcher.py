import os
import shutil


VERSIONS_LOCATION = "versions"
INSTALL_LOCATION = "install"
VERSION_FILE = os.path.join(INSTALL_LOCATION, "version.txt")


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


if __name__ == "__main__":
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
