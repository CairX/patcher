import lzma
import os
import shutil
import tarfile
import urllib.request

from configparser import ConfigParser


VERSION_FILE = ".version"
CHANGES_FILE = ".changes"


class Log(object):
	__levels = {}

	@classmethod
	def level(cls, level, value):
		cls.__levels[level] = value

	@classmethod
	def message(cls, level, message):
		if level in cls.__levels and cls.__levels[level]:
			print(message)


def update(install_path, server_info, server_versions):
	response = urllib.request.urlopen(server_info)
	versions = response.read().decode("utf-8").split("\n")

	if os.path.exists(install_path):
		version_path = os.path.join(install_path, VERSION_FILE)
		try:
			with open(version_path) as file:
				current = file.readline().strip()
		except OSError:
			Log.message("ERROR", "Can't access: " + version_path)
			return

		try:
			index = versions.index(current) + 1
		except ValueError:
			Log.message("ERROR", "Version mismatch.")
			return

		if index == len(versions):
			Log.message("INFO", "No new update.")
			return

		shutil.rmtree(install_path)

	version = versions[-1]
	Log.message("INFO", "Installing version " + str(version))

	tar_name = str(version) + ".tar.xz"
	tmp_dir = "tmp"
	os.mkdir(tmp_dir)
	tar_tmp = os.path.join(tmp_dir, tar_name)
	urllib.request.urlretrieve(server_versions + tar_name, tar_tmp)

	with lzma.open(tar_tmp) as f:
		with tarfile.open(fileobj=f) as tar:
			tar.extractall(install_path)

	os.remove(os.path.join(install_path, CHANGES_FILE))

	with open(os.path.join(install_path, VERSION_FILE), "w") as file:
		file.write(str(version))

	shutil.rmtree(tmp_dir)


if __name__ == "__main__":
	Log.level("INFO", True)
	Log.level("ERROR", True)

	config = ConfigParser()
	config.read("downloader.ini")
	local = config["local"]
	server = config["server"]

	update(local["install"], server["info"], server["versions"])
