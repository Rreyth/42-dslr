from sys import argv, stderr

if len(argv) != 3:
	print("Error: wrong number of arguments", file=stderr)
	print("Usage: python logreg_predict.py dataset_test.csv weights")
	exit(1)
 
if not argv[1].endswith("dataset_test.csv") or argv[2] != "weights":
	print("Error: arguments must be dataset_test.csv and weights", file=stderr)
	print("Usage: python logreg_predict.py dataset_test.csv weights")
	exit(1)
 
#get weights
#get data

#predict
#for each house
	# weights = weights for the actual house
	# b = weights.pop()

	# X = data.subMatrix(-1, 0) #maybe not since column 0 is supposedly house so empty here

	# tmp = X.dot(weights)
	# odds = [val + b for val in tmp]
	# pred = sigmoid(odds)
 
#compare each pred and take the most likeli house for each pers

#save final prediction to houses.csv (format : "index,Hogwarts House\n")