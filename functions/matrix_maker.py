import numpy as np
from itertools import islice
from classes import Data


NUMERICAL_VALUES_START = 6
NB_USELESS_COLUMNS = 2


def fill_matrix_row(row, data, stud, k):
	for key, value in islice(stud.items(), NUMERICAL_VALUES_START, None):
		if key != "Arithmancy" and key != "Care of Magical Creatures":
			if len(value) == 0:
				row[k] = data.get_col(key)["mean"]
			else:
				row[k] = float(value)
			k = k + 1


def make_matrix(data : Data, offset, name = 'none') -> np.ndarray :
	mat = np.ndarray((len(data.studs), len(data.studs[0]) - NUMERICAL_VALUES_START - NB_USELESS_COLUMNS + offset), dtype=float)
	for i, stud in enumerate(data.studs):
		if name != "none":
			mat[i, 0] = 1 if stud["Hogwarts House"] == name else 0
		k = offset
		fill_matrix_row(mat[i], data, stud, k)

	return mat
