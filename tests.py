import filecmp
import patcher
import os


def dircmp(lhs, rhs, ignore=[]):
	left = os.scandir(lhs)
	right = os.listdir(rhs)
	right = [entry for entry in right if entry not in ignore]

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
				right.remove(entry.name)
				if filecmp.cmp(entry.path, os.path.join(rhs, entry.name), shallow=False):
					match.append(entry.path)
				else:
					mismatch.append(entry.path)
			else:
				error.append(entry.path)
		elif entry.is_dir():
			if entry.name in right:
				right.remove(entry.name)
				results = dircmp(entry.path, os.path.join(rhs, entry.name))
				match.extend(results[0])
				mismatch.extend(results[1])
				error.extend(results[2])
			else:
				mismatch.append(entry.path)

	right = [os.path.join(rhs, entry) for entry in right]
	mismatch.extend(right)

	return (match, mismatch, error)


tests = sorted(os.listdir("tests"))
for test in tests:
	patcher.Log.level("INFO", False)
	patcher.Log.level("DETAILS", False)

	print("Test: " + test)
	versions = os.path.join("tests", test, "versions")
	install = os.path.join("tests", test, "result")

	if os.path.exists(install):
		patcher.uninstall(install)

	patcher.install("1", versions, install)
	patcher.update(versions, install)

	# TODO Remove the static here, might be multiple steps.
	results = dircmp(os.path.join(versions, "2"), install, ["changes.txt", "version.txt"])
	print("Match: " + str(len(results[0])))
	print("Mismatch: " + str(len(results[1])))
	for mismatch in results[1]:
		print("\t" + mismatch)
	print("Error:" + str(len(results[2])))
	for error in results[2]:
		print("\t" + error)
