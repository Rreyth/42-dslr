from sys import stderr, argv
from os import path, makedirs
from classes.Data import Data
from functions.myMath import list_abs
import matplotlib.pyplot as plt
import numpy as np
from itertools import islice
import argparse


def dirCreate():
	if path.isdir("Visualization"):
		return
	try:
		makedirs("Visualization")
	except Exception as e:
		print(f"Error: {e}", file=stderr)
		exit(1)


NUMERICAL_VALUES_START = 6
NB_USELESS_COLUMNS = 2


def make_matrix(data : Data, name : str) -> np.ndarray :
	mat = np.ndarray((len(data.studs), len(data.studs[0]) - NUMERICAL_VALUES_START - NB_USELESS_COLUMNS + 1), dtype=float)
	for i, stud in enumerate(data.studs):
		mat[i, 0] = 1 if stud["Hogwarts House"] == name else 0
		k = 1
		for key, value in islice(stud.items(), NUMERICAL_VALUES_START, None):
			if key != "Arithmancy" and key != "Care of Magical Creatures":
				if len(value) == 0:
					mat[i, k] = data.getCol(key)["mean"]
				else:
					mat[i, k] = float(value)
				k = k + 1

	return mat


def sigmoid(x):
	return 1 / (1 + np.exp(-x))


def init_GD(M: np.ndarray):
	y = M[:, 0].astype(dtype=int)
	X = np.delete(M, 0, axis=1)
	maxX = np.max(np.absolute(X), axis=0)
	X = X / maxX

	bias = np.ones(X.shape[0])
	X = np.column_stack((X, bias))

	return X, maxX, y, bias


def denormalize_weights(weights, maxX):
	last = weights[-1]
	weights = weights[:-1]
	denormalized_weights = weights * (1.0 / maxX)
	return np.append(denormalized_weights, last)


def compute_gradient(X, weights, y, learningRate, stochastic : bool):
	dot_product = np.dot(X, weights)
	pred = sigmoid(dot_product)
	sub = pred - y
	gradient = np.dot(X.T, sub)
	if not stochastic:
		gradient = gradient / len(y)
	gradient *= learningRate

	return gradient


error_lists = []

def gradient_descent(M: np.ndarray, learningRate, max_iter):
	error_lists.append([])
	X, maxX, y, bias = init_GD(M)
	weights = np.zeros(X.shape[1])

	for i in range(max_iter):
		gradient = compute_gradient(X, weights, y, learningRate, False)
		weights -= gradient

		error = sum(list_abs(gradient))
		error_lists[-1].append(error)

		if error < 1e-6: #convergence
			break

	return denormalize_weights(weights, maxX)


def stochastic_gradient_descent(M: np.ndarray, learningRate, max_iter):
	error_lists.append([])
	X, maxX, y, bias = init_GD(M)

	weights = np.zeros(X.shape[1])
	for i in range(max_iter):
		rand_index = np.random.randint(X.shape[0])
		rand_X = X[rand_index, :]
		rand_y = y[rand_index]

		gradient = compute_gradient(rand_X, weights, rand_y, learningRate, True)
		weights -= gradient

		error = sum(list_abs(gradient))
		error_lists[-1].append(error)

		if error < 1e-6: #convergence
			break

	return denormalize_weights(weights, maxX)


def mini_batch_gradient_descent(M: np.ndarray, learningRate, max_iter, batch_size):

	if batch_size < 1:
		batch_size = 1
	elif batch_size > M.shape[0]:
		batch_size = M.shape[0]

	error_lists.append([])
	X, maxX, y, bias = init_GD(M)

	weights = np.zeros(X.shape[1])
	for i in range(max_iter):
		rand_indexes = np.random.randint(X.shape[0], size=batch_size)
		rand_X = X[rand_indexes, :]
		rand_y = y[rand_indexes]

		gradient = compute_gradient(rand_X, weights, rand_y, learningRate, False)
		weights -= gradient

		error = sum(list_abs(gradient))
		error_lists[-1].append(error)

		if error < 1e-6: #convergence
			break

	return denormalize_weights(weights, maxX)


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

class IsCSVFile(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		if not values.endswith(".csv"):
			raise argparse.ArgumentError(self, f"'{values}' is not a csv file.")
		setattr(namespace, self.dest, values)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset", action=IsCSVFile, help="path to the dataset file")
	parser.add_argument("-gd", "--gradient_descent", choices=["batch", "stochastic", "minibatch"], help="gradient descent type")

	args = parser.parse_args()

	dirCreate()

	data = Data(argv[1])

	houses = [{'name': 'Gryffindor', 'matrix': make_matrix(data, "Gryffindor")},
			{'name': 'Ravenclaw', 'matrix': make_matrix(data, "Ravenclaw")},
			{'name': 'Slytherin', 'matrix': make_matrix(data, "Slytherin")},
			{'name': 'Hufflepuff', 'matrix': make_matrix(data, "Hufflepuff")}]

	save = ""
	fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(15, 15))
	for i, house in enumerate(houses):
		if args.gradient_descent == "stochastic":
			weights = stochastic_gradient_descent(house["matrix"], 0.01, 1000)
		elif args.gradient_descent == "minibatch":
			weights = mini_batch_gradient_descent(house["matrix"], 0.01, 1000, 16)
		else:
			weights = gradient_descent(house["matrix"], 0.01, 1000)
		save += f"{house['name']}\n{format_weights(weights)}\n"
		print(f"{house['name']}: 100%")

		# visualization of gradient descent
		x = i % 2
		y = i // 2
		axs[x, y].set(ylabel="Error", xlabel="Iterations")
		axs[x, y].set_title(house["name"], fontsize=20, pad=15)
		axs[x, y].yaxis.label.set_size(15)
		axs[x, y].xaxis.label.set_size(15)
		axs[x, y].plot(error_lists[i])

	save_weights(save)
	fig.savefig("Visualization/gradient_descent.png")


if __name__ == "__main__":
	main()
