import matplotlib.pyplot as plt
import numpy as np
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
	return 1 / (1 + np.exp(-x))

def gradient_descent(X, y, learningRate): # X -> matrix
	weights = np.zeros(X.shape[1]) #nb de column (donc de var)

	for _ in range(10000): #change en while true ? vu que ça break quand on atteint la precision max ?
		pred = sigmoid(np.dot(X, weights))
		gradient = np.dot(X.T, (pred - y)) / y.size
		weights -= learningRate * gradient
		
		if np.abs(gradient).sum() < 1e-6: #covergence -> les iterations suivantes sont useless
			break

	return weights

data = np.array([[5, 0], [7, 0], [10, 0], [12, 0], [14, 0], [13, 1], [15, 1], [16, 1], [18, 1], [20, 1]])

# plt.scatter(x=np.take(data, [0], 1), y=np.take(data, [1], 1))
# plt.show()

# weights = gradient_descent(np.take(data, [0], 1), np.take(data, [1], 1), 0.01) -> fonctionne pour plusieurs poids (matrice)

a = 0
b = 1

points = []
for point in data:
    odds = a * point[0] + b
    log_odds = m.log(odds)
    p = m.exp(log_odds) / (1 + m.exp(log_odds)) 
    points.append([point[0], p])
	
new_data = np.array(points)
print(new_data)
print("log likelihood =", likelihood(data, new_data))

plt.plot(np.take(new_data, [0], 1), np.take(new_data, [1], 1))
plt.show()