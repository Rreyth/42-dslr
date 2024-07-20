import matplotlib.pyplot as plt
import numpy as np
from classes.Matrix import Matrix
from functions.myMath import list_exp, list_abs
import math as m


# def likelihood(init_data, pred_data):
# 	res = 1
# 	for i in range(len(init_data)):
# 		if init_data[i][1] == 0:
# 			res *= (1 - pred_data[i][1])
# 		else:
# 			res *= pred_data[i][1]
   
# 	return res

def likelihood(init_data, pred_data):
	res = 0
	for i in range(len(init_data)):
		if init_data[i][1] == 0:
			res += m.log(1 - pred_data[i][1])
		else:
			res += m.log(pred_data[i][1])
   
	return res

# def sigmoid(x): #np.array
# 	return 1 / (1 + np.exp(-x))

# def gradient_descent(X, y, learningRate): # REDO WITH MY MATRIX + WITHOUT NUMPY
# 	weights = np.zeros(X.shape[1]) #nb de column (donc de var)

# 	for _ in range(10000): #change en while true ? vu que ça break quand on atteint la precision max ?
# 		pred = sigmoid(np.dot(X, weights))
# 		gradient = np.dot(X.T, (pred - y)) / y.size
# 		weights -= learningRate * gradient
		
# 		if np.abs(gradient).sum() < 1e-6: #covergence -> les iterations suivantes sont useless
# 			break

# 	return weights

def sigmoid(x):
	scaled_x = [elem * -1 for elem in x]
	expo = list_exp(scaled_x)
	res = []
	for i in range(len(expo)):
		res.append(1 / (1 + expo[i]))
  
	return res

def gradient_descent(M : Matrix, learningRate):
	X = M.subMatrix(-1, 0)
	y = M.colToLine(0)

	weights = [0.0 for i in range(X.size()[1])]
	# for i in range(10000):
	while True:
		pred = sigmoid(X.dot(weights))
		sub = [pred[j] - y[j] for j in range(len(y))]
		gradient = X.transpose().dot(sub)
		gradient = [value / len(y) for value in gradient]  
		weights = [weights[j] - (learningRate * gradient[j]) for j in range(len(weights))]

		if sum(list_abs(gradient)) < 1e-6: #convergence
			break

	return weights

# data = Matrix([[0, 5], [0, 7], [0, 10], [0, 12], [0, 14], [1, 13], [1, 15], [1, 16], [1, 18], [1, 20]])
data = Matrix([[0, 0.6], [0, 1.1], [0, 1.9], [0, 3.9], [1, 2.1], [1, 3.3], [1, 4.1], [1, 4.5], [1, 5.1]])
# print(data)

weights = gradient_descent(data, 0.01)
print(weights)
# tmp = data.subMatrix(-1, 0)
# print(tmp)

# plt.scatter(x=np.take(data, [0], 1), y=np.take(data, [1], 1))
# plt.show()

# weights = gradient_descent(np.take(data, [0], 1), np.take(data, [1], 1), 0.01) -> fonctionne pour plusieurs poids (matrice)

a = weights[0]
b = -1

points = []
for i in range(data.size()[0]):
	odds = a * data[i, 1] + b
	log_odds = m.log(odds)
	p = m.exp(log_odds) / (1 + m.exp(log_odds)) 
	points.append([p, data[i, 1]])
	
new_data = np.array(points)
# print(new_data)
# old_data = np.array([[0, 5], [0, 7], [0, 10], [0, 12], [0, 14], [1, 13], [1, 15], [1, 16], [1, 18], [1, 20]])
old_data = np.array([[0, 0.6], [0, 1.1], [0, 1.9], [0, 3.9], [1, 2.1], [1, 3.3], [1, 4.1], [1, 4.5], [1, 5.1]])
print("log likelihood =", likelihood(old_data, new_data))

plt.plot(np.take(new_data, [1], 1), np.take(new_data, [0], 1))
plt.show()