from sys import argv, stderr
from classes.Data import Data
from functions.describe_fcts import to_dict

import numpy as np
from itertools import islice

if len(argv) != 3:
	print("Error: wrong number of arguments", file=stderr)
	print("Usage: python logreg_predict.py */dataset_test.csv weights")
	exit(1)

if (argv[1] != "dataset_test.csv" and not argv[1].endswith("/dataset_test.csv"))\
		or (argv[2] != "weights" and not argv[2].endswith("/weights")):
	print("Error: arguments must be dataset_test.csv and weights", file=stderr)
	print("Usage: python logreg_predict.py */dataset_test.csv weights")
	exit(1)


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


NUMERICAL_VALUES_START = 6
NB_USELESS_COLUMNS = 2

def make_matrix(data : Data) -> np.ndarray :
	mat = np.ndarray((len(data.content), len(data.content[0]) - NUMERICAL_VALUES_START - NB_USELESS_COLUMNS), dtype=float)
	for i, stud in enumerate(data.content):
		k = 0
		for key, value in islice(stud.items(), NUMERICAL_VALUES_START, None):
			if (key != "Arithmancy" and key != "Care of Magical Creatures"):
				if len(value) == 0:
					mat[i, k] = data.getCol(key)["mean"]
				else:
					mat[i, k] = float(value)
				k = k + 1

	return mat


def make_houses(path):
	try:
		file = open(path)
	except Exception as e:
		print(f"Error: {e}", file=stderr)
		exit(1)
	content = [line.split(",") for line in file.read().splitlines()]
	houses = [{'name': content.pop(0)[0], 'weights': content.pop(0)}]
	houses.append({'name': content.pop(0)[0], 'weights': content.pop(0)})
	houses.append({'name': content.pop(0)[0], 'weights': content.pop(0)})
	houses.append({'name': content.pop(0)[0], 'weights': content.pop(0)})

	return houses


def choose_house(houses, nbStuds):
	res = []

	tmpHouse = 'none'

	for i in range(nbStuds):
		likelihood = -1000
		for house in houses:
			if house['likelihood'][i] >= likelihood:
				likelihood = house['likelihood'][i]
				tmpHouse = house['name']
		res.append(tmpHouse)

	return res


def sigmoid(x):
	return 1 / (1 + np.exp(-x))


def save_houses(houses):
	try:
		file = open("houses.csv", 'x+t')
	except Exception as e:
		try:
			file = open("houses.csv", 'w+t')
		except Exception as e:
			print(f"Error: {e}", file=stderr)
			exit(1)

	save = "Index,Hogwarts House\n"
	for i, house in enumerate(houses):
		save += f"{i},{house}\n"
	file.write(save)


houses = make_houses(argv[2])

data = get_data(argv[1])

matrix = make_matrix(data)

predict = []
for house in houses:
	weights = [float(w) for w in house['weights']]

	b = weights.pop()

	odds = np.dot(matrix, weights) + b
	predict.append({'name' : house['name'], 'likelihood' : sigmoid(odds)})


final_prediction = choose_house(predict, matrix.shape[0])

save_houses(final_prediction)
