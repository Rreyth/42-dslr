import argparse
import numpy as np
from classes.Data import Data
from functions.myMath import sigmoid
from functions.file_utils import save_houses, make_houses, IsCSVFile
from functions.matrix_maker import make_matrix


def choose_house(houses, nb_studs):
	res = []

	tmp_house = 'none'

	for i in range(nb_studs):
		likelihood = -1000
		for house in houses:
			if house['likelihood'][i] >= likelihood:
				likelihood = house['likelihood'][i]
				tmp_house = house['name']
		res.append(tmp_house)

	return res


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset", action=IsCSVFile, help="path to the dataset file")
	parser.add_argument("weights", help="path to the weights file")

	args = parser.parse_args()

	houses = make_houses(args.weights)
	data = Data(args.dataset)
	matrix = make_matrix(data, 0)

	predict = []
	for house in houses:
		weights = [float(w) for w in house['weights']]

		b = weights.pop()

		odds = np.dot(matrix, weights) + b
		predict.append({'name': house['name'], 'likelihood': sigmoid(odds)})

	final_prediction = choose_house(predict, matrix.shape[0])

	save_houses(final_prediction)


if __name__ == "__main__":
	main()
