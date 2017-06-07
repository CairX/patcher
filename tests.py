import filecmp
import patcher
import os

from collections import namedtuple

Result = namedtuple("Result", ["match", "mismatch", "error"])


def dircmp(lhs, rhs, ignore=[], parent=None):
	lhs_entries = os.listdir(lhs)
	lhs_entries = [e for e in lhs_entries if e not in ignore]

	rhs_entries = os.listdir(rhs)
	rhs_entries = [e for e in rhs_entries if e not in ignore]

	compare = set(lhs_entries).intersection(rhs_entries)

	result = Result([], [], [])
	result.error.extend([os.path.join(lhs, e) for e in lhs_entries if e not in compare])
	result.error.extend([os.path.join(rhs, e) for e in rhs_entries if e not in compare])

	for entry in compare:
		lhs_entry = os.path.join(lhs, entry)
		rhs_entry = os.path.join(rhs, entry)
		relative_entry = os.path.join(parent, entry) if parent else entry

		if os.path.isfile(lhs_entry):
			if filecmp.cmp(lhs_entry, rhs_entry, shallow=False):
				result.match.append(relative_entry)
			else:
				result.mismatch.append(relative_entry)
		else:
			entry_result = dircmp(lhs_entry, rhs_entry, parent=relative_entry)
			result.match.append(relative_entry)
			result.match.extend(entry_result.match)
			result.mismatch.extend(entry_result.mismatch)
			result.error.extend(entry_result.error)

	return result


def dirtest(directory):
	versions = os.path.join(directory, "versions")
	install = os.path.join(directory, "result")

	if os.path.exists(install):
		patcher.uninstall(install)

	patcher.install("1", versions, install)
	patcher.update(versions, install)

	# TODO Remove the static here, might be multiple steps.
	result = dircmp(os.path.join(versions, "2"), install, [patcher.CHANGES_FILE, patcher.VERSION_FILE])

	excepted = False
	with open(os.path.join(directory, "expected.txt")) as file:
		exp = file.readlines()
		exp = [entry.strip() for entry in exp]
		excepted = exp == result.match

	passed = excepted and len(result.mismatch) == 0 and len(result.error) == 0
	print(("passed" if passed else "failed") + ": " + directory)
	if not passed:
		print("Match: " + str(len(result.match)))
		for match in result.match:
			print("\t" + match)
		print("Mismatch: " + str(len(result.mismatch)))
		for mismatch in result.mismatch:
			print("\t" + mismatch)
		print("Error:" + str(len(result.error)))
		for error in result.error:
			print("\t" + error)


def run():
	tests = []
	for root, dirs, files in os.walk("tests"):
		if "versions" in dirs:
			tests.append(root)

	for test in sorted(tests):
		dirtest(test)


if __name__ == "__main__":
	patcher.Log.level("INFO", False)
	patcher.Log.level("DETAILS", False)
	patcher.Log.level("WARNING", True)
	run()
