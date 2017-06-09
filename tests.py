import compare
import os
import patcher


def dirtest(directory):
	versions = os.path.join(directory, "versions")
	install = os.path.join(directory, "result")

	if os.path.exists(install):
		patcher.uninstall(install)

	patcher.install("1", versions, install)
	patcher.update(versions, install)

	# TODO Remove the static here, might be multiple steps.
	result = compare.dircmp(os.path.join(versions, "2"), install, [patcher.CHANGES_FILE, patcher.VERSION_FILE])

	excepted = False
	with open(os.path.join(directory, "expected.txt")) as file:
		exp = file.readlines()
		exp = [patcher.prepare_path(entry) for entry in exp]
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
