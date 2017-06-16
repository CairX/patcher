import lzma
import os
import shutil
import tarfile
import urllib.request

from configparser import ConfigParser
from log import Log


VERSION_FILE = ".version"
CHANGES_FILE = ".changes"


def get_server_version(server_info):
	response = urllib.request.urlopen(server_info)
	versions = response.read().decode("utf-8").split("\n")
	return versions[-1]


def get_local_version(install_path):
	if not os.path.exists(install_path):
		Log.message("WARNING", "Install path doesn't exist: " + install_path)
		return 0

	version_path = os.path.join(install_path, VERSION_FILE)
	if not os.path.exists(version_path):
		Log.message("WARNING", "Install version-file doesn't exist: " + install_path)
		return 0

	try:
		with open(version_path) as file:
			current = file.readline().strip()
	except OSError:
		Log.message("WARNING", "Can't access: " + version_path)
		return 0

	return current


def install(install_path, server_versions, version):
	Log.message("INFO", "Installing version " + str(version))

	if os.path.exists(install_path):
		shutil.rmtree(install_path)

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


def update(install_path, server_info, server_versions):
	server_version = get_server_version(server_info)
	local_version = get_local_version(install_path)

	if local_version == server_version:
		Log.message("INFO", "No updates.")
	else:
		install(install_path, server_versions, server_version)


if __name__ == "__main__":
	Log.level("INFO", True)
	Log.level("WARNING", True)
	Log.level("ERROR", True)

	config = ConfigParser()
	config.read("downloader.ini")
	local = config["local"]
	server = config["server"]

	update(local["install"], server["info"], server["versions"])
