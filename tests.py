import filecmp
import patcher
import os


def dircmp(lhs, rhs, ignore=[], parent=None):
	left = os.scandir(lhs)
	right = os.listdir(rhs)
	right = [entry for entry in right if entry not in ignore]

	# TODO Support the testing of sub-folders
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
					match.append(os.path.join(parent, entry.name) if parent else entry.name)
				else:
					mismatch.append(entry.path)
			else:
				error.append(entry.path)
		elif entry.is_dir():
			if entry.name in right:
				match.append(os.path.join(parent, entry.name) if parent else entry.name)
				right.remove(entry.name)
				dirparent = os.path.join(parent, entry.name) if parent else entry.name

				results = dircmp(entry.path, os.path.join(rhs, entry.name), [".keep"], dirparent)
				match.extend(results[0])
				mismatch.extend(results[1])
				error.extend(results[2])
			else:
				mismatch.append(entry.path)

	right = [os.path.join(rhs, entry) for entry in right]
	error.extend(right)

	return (match, mismatch, error)


def test(directory):
	patcher.Log.level("INFO", False)
	patcher.Log.level("DETAILS", False)
	patcher.Log.level("WARNING", True)

	versions = os.path.join(directory, "versions")
	install = os.path.join(directory, "result")

	if os.path.exists(install):
		patcher.uninstall(install)

	patcher.install("1", versions, install)
	patcher.update(versions, install)

	# TODO Remove the static here, might be multiple steps.
	results = dircmp(os.path.join(versions, "2"), install, ["changes.txt", "version.txt", ".keep"])

	excepted = False
	with open(os.path.join(directory, "expected.txt")) as file:
		exp = file.readlines()
		exp = [entry.strip() for entry in exp]
		excepted = exp == results[0]

	passed = excepted and len(results[1]) == 0 and len(results[2]) == 0
	print(("passed" if passed else "failed") + ": " + directory)
	if not passed:
		print("Match: " + str(len(results[0])))
		for match in results[0]:
			print("\t" + match)
		print("Mismatch: " + str(len(results[1])))
		for mismatch in results[1]:
			print("\t" + mismatch)
		print("Error:" + str(len(results[2])))
		for error in results[2]:
			print("\t" + error)


def run():
	for root, dirs, files in os.walk("tests"):
		if "versions" in dirs:
			test(root)


if __name__ == "__main__":
	run()
