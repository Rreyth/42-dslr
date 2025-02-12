import argparse
import numpy as np
import matplotlib.pyplot as plt
from classes.Data import Data
from functions.myMath import list_abs, sigmoid
from functions.file_utils import save_weights, dir_create, IsCSVFile
from functions.matrix_maker import make_matrix


def init_GD(M: np.ndarray):
	y = M[:, 0].astype(dtype=int)
	X = np.delete(M, 0, axis=1)
	max_x = np.max(np.absolute(X), axis=0)
	X = X / max_x

	bias = np.ones(X.shape[0])
	X = np.column_stack((X, bias))

	return X, max_x, y


def denormalize_weights(weights, max_x):
	last = weights[-1]
	weights = weights[:-1]
	denormalized_weights = weights * (1.0 / max_x)
	return np.append(denormalized_weights, last)


def compute_gradient(X, weights, y, learning_rate, stochastic : bool):
	dot_product = np.dot(X, weights)
	pred = sigmoid(dot_product)
	sub = pred - y
	gradient = np.dot(X.T, sub)
	if not stochastic:
		gradient = gradient / len(y)
	gradient *= learning_rate

	return gradient


def gradient_descent(M: np.ndarray, learning_rate, max_iter):
	errors = []
	X, max_x, y = init_GD(M)
	weights = np.zeros(X.shape[1])

	for i in range(max_iter):
		gradient = compute_gradient(X, weights, y, learning_rate, False)
		weights -= gradient

		error = sum(list_abs(gradient))
		errors.append(error)

		if error < 1e-6: #convergence
			break

	return denormalize_weights(weights, max_x), errors


def stochastic_gradient_descent(M: np.ndarray, learning_rate, max_iter):
	errors = []
	X, max_x, y = init_GD(M)

	weights = np.zeros(X.shape[1])
	for i in range(max_iter):
		rand_index = np.random.randint(X.shape[0])
		rand_X = X[rand_index, :]
		rand_y = y[rand_index]

		gradient = compute_gradient(rand_X, weights, rand_y, learning_rate, True)
		weights -= gradient

		error = sum(list_abs(gradient))
		errors.append(error)

		if error < 1e-6: #convergence
			break

	return denormalize_weights(weights, max_x), errors


def mini_batch_gradient_descent(M: np.ndarray, learning_rate, max_iter, batch_size):

	if batch_size < 1:
		batch_size = 1
	elif batch_size > M.shape[0]:
		batch_size = M.shape[0]

	errors = []
	X, max_x, y = init_GD(M)

	weights = np.zeros(X.shape[1])
	for i in range(max_iter):
		rand_indexes = np.random.randint(X.shape[0], size=batch_size)
		rand_X = X[rand_indexes, :]
		rand_y = y[rand_indexes]

		gradient = compute_gradient(rand_X, weights, rand_y, learning_rate, False)
		weights -= gradient

		error = sum(list_abs(gradient))
		errors.append(error)

		if error < 1e-6: #convergence
			break

	return denormalize_weights(weights, max_x), errors


def format_weights(weights):
	res = ""
	for i, w in enumerate(weights):
		res += str(w)
		res += "," if i != (len(weights) - 1) else ""
	return res


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset", action=IsCSVFile, help="path to the dataset file")
	parser.add_argument("-gd", "--gradient_descent", choices=["batch", "stochastic", "minibatch"], help="gradient descent type")

	args = parser.parse_args()

	dir_create("Visualization")

	data = Data(args.dataset)

	houses = [{'name': 'Gryffindor', 'matrix': make_matrix(data, 1, "Gryffindor")},
			{'name': 'Ravenclaw', 'matrix': make_matrix(data, 1, "Ravenclaw")},
			{'name': 'Slytherin', 'matrix': make_matrix(data, 1, "Slytherin")},
			{'name': 'Hufflepuff', 'matrix': make_matrix(data, 1, "Hufflepuff")}]

	save = ""
	fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(15, 15))
	for i, house in enumerate(houses):
		if args.gradient_descent == "stochastic":
			weights, errors = stochastic_gradient_descent(house["matrix"], 0.01, 1000)
		elif args.gradient_descent == "minibatch":
			weights, errors = mini_batch_gradient_descent(house["matrix"], 0.01, 1000, 16)
		else:
			weights, errors = gradient_descent(house["matrix"], 0.01, 1000)
		save += f"{house['name']}\n{format_weights(weights)}\n"
		print(f"{house['name']}: 100%")

		# visualization of gradient descent
		x = i % 2
		y = i // 2
		axs[x, y].set(ylabel="Error", xlabel="Iterations")
		axs[x, y].set_title(house["name"], fontsize=20, pad=15)
		axs[x, y].yaxis.label.set_size(15)
		axs[x, y].xaxis.label.set_size(15)
		axs[x, y].plot(errors)

	save_weights(save)
	fig.savefig("Visualization/gradient_descent.png")


if __name__ == "__main__":
	main()
