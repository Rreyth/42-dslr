from sys import argv, stderr
# from classes.Data import Data
# from classes.Matrix import Matrix
# from functions.myMath import list_exp

if len(argv) != 3:
	print("Error: wrong number of arguments", file=stderr)
	print("Usage: python logreg_predict.py */dataset_test.csv weights")
	exit(1)

if (argv[1] != "dataset_test.csv" and not argv[1].endswith("/dataset_test.csv")) or argv[2] != "weights":
	print("Error: arguments must be dataset_test.csv and weights", file=stderr)
	print("Usage: python logreg_predict.py */dataset_test.csv weights")
	exit(1)

# def get_data(dataset):
# 	try:
# 		file = open(dataset)
# 	except Exception as e:
# 		print(f"Error: {e}", file=stderr)
# 		exit(1)
# 	content = [line.split(",") for line in file.read().splitlines()]
# 	names = content.pop(0)
# 	for i in range(len(content)):
# 		content[i] = to_dict(names, content[i])
# 	data = Data(content)

# 	return data

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

# def sigmoid(x):
# 	scaled_x = [elem * -1 for elem in x]
# 	expo = list_exp(scaled_x)
# 	res = []
# 	for i in range(len(expo)):
# 		res.append(1 / (1 + expo[i]))

# 	return res

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
print(houses) # TODO: remove

#get data

#data to matrix
#matrix = make_matrix(data) -> skip house column

predict = []
for house in houses:
	# weights = weights for the actual house -> house['weight]
	b = house['weights'].pop()

	# X = matrix.subMatrix(-1, 0) #maybe not since column 0 is supposedly house so empty here

	# odds = [val + b for val in X.dot(weights)]
	# predict.append({'house' : house['name'], 'likelihood' : sigmoid(odds)})

#compare each pred and take the most likely house for each pers
#final_prediction = choose_house(predict) -> list of houses

# save_houses(final_prediction)
