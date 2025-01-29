from sys import stderr, argv
from classes.Data import Data
from classes.Matrix import Matrix
from functions.describe_fcts import to_dict
from functions.myMath import list_exp, list_abs

import numpy as np

def make_matrix(data : Data, name : str) -> Matrix :
	mat = []
	for i, stud in enumerate(data.content):
		mat.append([])
		mat[i].append(1 if stud["Hogwarts House"] == name else 0)
		for id, value in stud.items():
			if id == "Index" or id == "Arithmancy" or id == "Care of Magical Creatures":
				continue
			try:
				grade = float(value)
				if grade != grade or grade == float('inf') or grade == float('-inf'):
					continue
				mat[i].append(grade)
			except Exception:
				if len(value) == 0:
					mat[i].append(data.getCol(id)["mean"])

	return Matrix(mat)

def make_matrix2(data : Data, name : str) -> np.ndarray :
	mat = np.ndarray((len(data.content), len(data.content[0]) - 6 - 2 + 1))
	student_count = 0
	for i, stud in enumerate(data.content):
		mat[i, 0] = 1 if stud["Hogwarts House"] == name else 0
		student_count = student_count + 1
		k = 1
		for j, (key, value) in enumerate(stud.items()):
			if (j > 6 and j != 16):
				if len(value) == 0:
					mat[i, k] = data.getCol(key)["mean"] # faire la moyenne par maison
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
	scaled_x = [elem * -1 for elem in x]
	expo = list_exp(scaled_x)
	res = []
	for i in range(len(expo)):
		res.append(1 / (1 + expo[i]))

	return res

def denormalise_weights(weights, maxes):
	res = []
	for i in range(len(weights) - 1):
		res.append(weights[i] * (1 / maxes[i]))
	return res

def gradient_descent(M: Matrix, M2: np.ndarray, learningRate, max_iter):
	y = M.colToLine(0)
	y2 = M2[:, 0].astype(dtype=int)
	X = M.subMatrix(-1, 0)
	X2 = np.delete(M2, 0, axis=1)
	X.normMatrix()
	X2 = (X2 - np.min(X2)) / (np.max(X2) - np.min(X2))

	bias = [1 for i in range(X.size()[0])]
	X.addCol(bias)

	weights = [0.0 for i in range(X.size()[1])]
	weights = np.asarray(weights)
	X = np.asarray(X)
	for i in range(max_iter):
		pred = sigmoid(X.dot(weights))
		sub = [pred[j] - y[j] for j in range(len(y))]
		gradient = X.transpose().dot(sub)
		gradient = [value / len(y) for value in gradient]
		weights = [weights[j] - (learningRate * gradient[j]) for j in range(len(weights))]

		if sum(list_abs(gradient)) < 1e-6: #convergence
			break

	denormalised_weights = denormalise_weights(weights, X.maxes)
	denormalised_weights.append(weights.pop())
	return denormalised_weights

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
houses.append({'name': 'Gryffindor', 'matrix': make_matrix(data, "Gryffindor"), 'matrix2': make_matrix2(data, "Gryffindor")})
houses.append({'name': 'Ravenclaw', 'matrix': make_matrix(data, "Ravenclaw"), 'matrix2': make_matrix2(data, "Ravenclaw")})
houses.append({'name': 'Slytherin', 'matrix': make_matrix(data, "Slytherin"), 'matrix2': make_matrix2(data, "Slytherin")})
houses.append({'name': 'Hufflepuff', 'matrix': make_matrix(data, "Hufflepuff"), 'matrix2': make_matrix2(data, "Hufflepuff")})

save = ""
for house in houses:
	weights = gradient_descent(house["matrix"], house["matrix2"], 0.1, 1000)
	save += f"{house['name']}\n{format_weights(weights)}\n"

save_weights(save)
