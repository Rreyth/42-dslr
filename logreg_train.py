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

	bias = [1 for i in range(X.size()[0])]
	X.addCol(bias)

	weights = [0.0 for i in range(X.size()[1])]
	while True:
		pred = sigmoid(X.dot(weights))
		sub = [pred[j] - y[j] for j in range(len(y))]
		gradient = X.transpose().dot(sub)
		gradient = [value / len(y) for value in gradient]  
		weights = [weights[j] - (learningRate * gradient[j]) for j in range(len(weights))]

		if sum(list_abs(gradient)) < 1e-6: #convergence #add condition pour un max d'iteration ?
			break

	return weights

data = Matrix([[0, 5], [0, 7], [0, 10], [0, 12], [0, 14], [1, 13], [1, 15], [1, 16], [1, 18], [1, 20]])
# data = Matrix([[0, 0.6], [0, 1.1], [0, 1.9], [0, 3.9], [1, 2.1], [1, 3.3], [1, 4.1], [1, 4.5], [1, 5.1]])
# print(data)

weights = gradient_descent(data, 0.01)
print(weights)

a = weights[0]
b = weights.pop()

X = data.subMatrix(-1, 0)
y = data.colToLine(0)

tmp = X.dot(weights)
odds = [val + b for val in tmp]
sig = sigmoid(odds)
pred = [[sig[i], data[i, 1]] for i in range(len(sig))]

new_data = np.array(pred)
# print(new_data)
old_data = np.array([[0, 5], [0, 7], [0, 10], [0, 12], [0, 14], [1, 13], [1, 15], [1, 16], [1, 18], [1, 20]])
# old_data = np.array([[0, 0.6], [0, 1.1], [0, 1.9], [0, 3.9], [1, 2.1], [1, 3.3], [1, 4.1], [1, 4.5], [1, 5.1]])
print("log likelihood =", likelihood(old_data, new_data))

plt.scatter(x=np.take(old_data, [1], 1), y=np.take(old_data, [0], 1), label="data")
plt.plot(np.take(new_data, [1], 1), np.take(new_data, [0], 1), label="pred", color="red")
# plt.scatter(np.take(new_data, [1], 1), np.take(new_data, [0], 1), label="pred", color="red")
plt.xlabel("value")
plt.ylabel("proba")
plt.legend()
plt.show()