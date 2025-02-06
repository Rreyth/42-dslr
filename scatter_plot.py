import matplotlib.pyplot as plt
from classes.Data import Data
from functions.file_utils import dir_create


def main():
	dir_create("Visualization")
	data = Data("datasets/dataset_train.csv")

	fig, axs = plt.subplots()

	axs.set(xlabel='Defense Against the Dark Arts', ylabel='Astronomy')

	x_data = data.allHouses['Defense Against the Dark Arts']
	y_data = data.allHouses['Astronomy']

	axs.scatter(x_data, y_data)

	fig.savefig("Visualization/scatter_plot.png")


if __name__ == "__main__":
	main()
