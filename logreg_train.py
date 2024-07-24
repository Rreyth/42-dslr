import matplotlib.pyplot as plt
from classes.Matrix import Matrix
from classes.Data import Data
from functions.myMath import list_exp, list_abs
from functions.describe_fcts import to_dict
import math as m
from sys import stderr, argv

def make_matrix(data : Data, name : str) -> Matrix :
	mat = []
	for i, stud in enumerate(data.content):
		mat.append([])
		mat[i].append(1 if stud["Hogwarts House"] == name else 0)
		for id, value in stud.items():
			if id == "Index":
				continue
			try:
				grade = float(value)
				mat[i].append(grade)
			except Exception:
				if len(value) == 0:
					mat[i].append(data.getCol(id)["mean"])
 
	return Matrix(mat)

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

# def likelihood(init_data, pred_data):
# 	res = 1
# 	for i in range(init_data.size()[0]):
# 		if init_data[i, 0] == 0:
# 			res *= (1 - pred_data[i, 0])
# 		else:
# 			res *= pred_data[i, 0]
   
# 	return res

def likelihood(init_data, pred_data):
	res = 0
	for i in range(init_data.size()[0]):
		if init_data[i, 0] == 0:
			res += m.log(1 - pred_data[i, 0])
		else:
			res += m.log(pred_data[i, 0])
   
	return res

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

def gradient_descent(M : Matrix, learningRate, max_iter):
	y = M.colToLine(0)
	X = M.subMatrix(-1, 0)
	X.normMatrix()

	bias = [1 for i in range(X.size()[0])]
	X.addCol(bias)

	weights = [0.0 for i in range(X.size()[1])]
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

def save_weights(weights):
	file = False
	try:
		file = open("weights", 'x+t')	
	except Exception as e:
		try:
			file = open("weights", 'w+t')
		except Exception as e:
			print(f"Error: {e}", file=stderr)
			exit(1)
  
	save = ""
	for w in weights:
		save += str(w) + "\n"
  
	file.write(save)

if len(argv) != 2:
	print("Error: wrong number of arguments", file=stderr)
	print("Usage: python logreg_train.py dataset_train.csv")
	exit(1)

if not argv[1].endswith(".csv"): #only take dataset_train.csv
	print("Error: argument must be dataset_train.csv", file=stderr)
	print("Usage: python logreg_train.py dataset_train.csv")
	exit(1)

# data = Matrix([[0, 5, 0.5], [0, 7, 1.1], [0, 10, 1.9], [0, 12, 2], [0, 14, 3.9], [1, 13, 2.1], [1, 15, 3.3], [1, 16, 4.1], [1, 18, 4.5], [1, 20, 5.1]])
data = Matrix([[0, 0.6], [0, 1.1], [0, 1.9], [0, 3.9], [1, 2.1], [1, 3.3], [1, 4.1], [1, 4.5], [1, 5.1]])

data = get_data(argv[1])
gryffindor_matrix = make_matrix(data, "Gryffindor")
# ravenclaw_matrix = make_matrix(data, "Ravenclaw")
# slytherin_matrix = make_matrix(data, "Slytherin")
# hufflepuff_matrix = make_matrix(data, "Hufflepuff")

# print(f"Gryffindor\n{gryffindor_matrix}")
# print(f"Ravenclaw\n{ravenclaw_matrix}")
# print(f"Slytherin\n{slytherin_matrix}")
# print(f"Hufflepuff\n{hufflepuff_matrix}")

# print(data)
weights = gradient_descent(gryffindor_matrix, 0.01, 100000)
print(weights)
# exit()
# save_weights(weights)

# b = weights.pop()

# X = data.subMatrix(-1, 0)
# y = data.colToLine(0)

# tmp = X.dot(weights)
# odds = [val + b for val in tmp]
# sig = sigmoid(odds)
# pred = Matrix([[sig[i], data[i, 1]] for i in range(len(sig))])

# print("log likelihood =", likelihood(data, pred))

# plt.scatter(x=data.colToLine(1), y=data.colToLine(0), label="data")
# plt.plot(pred.colToLine(1), pred.colToLine(0), label="pred", color="red")
# # plt.scatter(pred.colToLine(1), pred.colToLine(0), label="pred", color="red")

# plt.xlabel("value")
# plt.ylabel("proba")
# plt.legend()
# plt.show()