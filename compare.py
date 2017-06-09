import filecmp
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
