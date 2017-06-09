import filecmp
import os

from collections import namedtuple

Result = namedtuple("Result", ["match", "mismatch", "error"])


class Item(object):
	def __init__(self, lhs, rhs, relative):
		self.lhs = lhs
		self.rhs = rhs
		self.relative = relative

	def __str__(self):
		return "(" + str(self.lhs) + ", " + str(self.rhs) + ")"


def dircmp(lhs, rhs, ignore=[], parent=""):
	lhs_entries = os.listdir(lhs)
	lhs_entries = [e for e in lhs_entries if e not in ignore]

	rhs_entries = os.listdir(rhs)
	rhs_entries = [e for e in rhs_entries if e not in ignore]

	compare = set(lhs_entries).intersection(rhs_entries)

	result = Result([], [], [])
	result.error.extend([Item(os.path.join(lhs, e), None, os.path.join(parent, e)) for e in lhs_entries if e not in compare])
	result.error.extend([Item(None, os.path.join(rhs, e), os.path.join(parent, e)) for e in rhs_entries if e not in compare])

	for entry in compare:
		lhs_entry = os.path.join(lhs, entry)
		rhs_entry = os.path.join(rhs, entry)
		relative_entry = os.path.join(parent, entry)

		if os.path.isfile(lhs_entry):
			if filecmp.cmp(lhs_entry, rhs_entry, shallow=False):
				result.match.append(Item(lhs_entry, rhs_entry, relative_entry))
			else:
				result.mismatch.append(Item(lhs_entry, rhs_entry, relative_entry))
		else:
			entry_result = dircmp(lhs_entry, rhs_entry, parent=relative_entry)
			result.match.append(Item(lhs_entry, rhs_entry, relative_entry))
			result.match.extend(entry_result.match)
			result.mismatch.extend(entry_result.mismatch)
			result.error.extend(entry_result.error)

	return result
