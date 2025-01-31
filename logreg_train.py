from sys import stderr, argv
from classes.Data import Data
from functions.describe_fcts import to_dict
from functions.myMath import list_abs

import numpy as np
from itertools import islice

NUMERICAL_VALUES_START = 6
NB_USELESS_COLUMNS = 2

def make_matrix(data : Data, name : str) -> np.ndarray :
	mat = np.ndarray((len(data.content), len(data.content[0]) - NUMERICAL_VALUES_START - NB_USELESS_COLUMNS + 1), dtype=float)
	for i, stud in enumerate(data.content):
		mat[i, 0] = 1 if stud["Hogwarts House"] == name else 0
		k = 1
		for key, value in islice(stud.items(), NUMERICAL_VALUES_START, None):
			if (key != "Arithmancy" and key != "Care of Magical Creatures"):
				if len(value) == 0:
					mat[i, k] = data.getCol(key)["mean"]
				else:
					mat[i, k] = float(value)
				k = k + 1

	return mat

def get_data(dataset):
	try:
		file = open(dataset)
	except Exception as e:
		print(f"Error: {e}", file=stderr)
		exit(1)
	content = [line.split(",") for line in file.read().splitlines()]
	names = content.pop(0)
	for i in range(len(content)):
		content[i] = to_dict(names, content[i])
	data = Data(content)

	return data

def sigmoid(x):
	return 1 / (1 + np.exp(-x))

def gradient_descent(M: np.ndarray, learningRate, max_iter):
	y = M[:, 0].astype(dtype=int)
	X = np.delete(M, 0, axis=1)
	minX = X.min(axis=0)
	maxX = np.max(np.absolute(X), axis=0)
	# X = (X - minX) / (maxX - minX)
	X = X / maxX

	bias = np.ones(X.shape[0])
	X = np.column_stack((X, bias))

	weights = np.zeros(X.shape[1])
	for i in range(max_iter):
		dot_product = np.dot(X, weights)
		pred = sigmoid(dot_product)
		sub = pred - y
		gradient = np.dot(X.T, sub)
		gradient = gradient / len(y)
		gradient *= learningRate
		weights -= gradient

		if sum(list_abs(gradient)) < 1e-6: #convergence
			break

	last = weights[-1]
	weights = weights[:-1]
	denormalised_weights = weights * (1.0 / maxX)
	return np.append(denormalised_weights, last)

def save_weights(save):
	file = False
	try:
		file = open("weights", 'x+t')
	except Exception as e:
		try:
			file = open("weights", 'w+t')
		except Exception as e:
			print(f"Error: {e}", file=stderr)
			exit(1)

	file.write(save)

def format_weights(weights):
	res = ""
	for i, w in enumerate(weights):
		res += str(w)
		res += "," if i != (len(weights) - 1) else ""
	return res

if len(argv) != 2:
	print("Error: wrong number of arguments", file=stderr)
	print("Usage: python logreg_train.py dataset_train.csv")
	exit(1)

if argv[1] != "dataset_train.csv" and not argv[1].endswith("/dataset_train.csv"):
	print("Error: argument must be dataset_train.csv", file=stderr)
	print("Usage: python logreg_train.py */dataset_train.csv")
	exit(1)

data = get_data(argv[1])
houses = []
houses.append({'name': 'Gryffindor', 'matrix': make_matrix(data, "Gryffindor")})
houses.append({'name': 'Ravenclaw', 'matrix': make_matrix(data, "Ravenclaw")})
houses.append({'name': 'Slytherin', 'matrix': make_matrix(data, "Slytherin")})
houses.append({'name': 'Hufflepuff', 'matrix': make_matrix(data, "Hufflepuff")})

save = ""
for house in houses:
	weights = gradient_descent(house["matrix"], 0.1, 1000)
	save += f"{house['name']}\n{format_weights(weights)}\n"
	print(f"{house['name']}: 100%")

save_weights(save)
