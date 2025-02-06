import numpy as np


def list_abs(values):
	res = []
	for value in values:
		res.append(value if value >= 0 else -value)
	return res


def sigmoid(x):
	return 1 / (1 + np.exp(-x))
