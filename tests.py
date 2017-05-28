import filecmp
import patcher
import os


def dircmp(lhs, rhs, ignore=[]):
	left = os.scandir(lhs)
	right = os.listdir(rhs)

	# TODOD Support the testing of sub-folders
	# TODO Sort either file or folders first
	# TODO Sort in alphabetic order

	match = []
	mismatch = []
	error = []

	for entry in left:
		if entry.is_file():
			if entry.name in ignore:
				continue

			if entry.name in right:
				if filecmp.cmp(entry.path, os.path.join(rhs, entry.name), shallow=False):
					match.append(entry.path)
				else:
					mismatch.append(entry.path)
			else:
				error.append(entry.path)

	return (match, mismatch, error)


for test in os.listdir("tests"):
	print("Test: " + test)
	versions = os.path.join("tests", test, "versions")
	install = os.path.join("tests", test, "result")

	if os.path.exists(install):
		patcher.uninstall(install)

	patcher.install("1", versions, install)
	patcher.update(versions, install)

	# TODO Remove the static here, might be multiple steps.
	results = dircmp(os.path.join(versions, "2"), install, ["changes.txt"])
	print("Passed: " + str(len(results[0])))
	print("Failed: " + str(len(results[1]) + len(results[2])))
