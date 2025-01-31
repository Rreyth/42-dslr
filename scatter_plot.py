from os import path, makedirs
from sys import stderr
import matplotlib.pyplot as plt
from classes.Data import Data

def dirCreate():
	if path.isdir("Visualization"):
		return
	try:
		makedirs("Visualization")
	except Exception as e:
		print(f"Error: {e}", file=stderr)
		exit(1)


if __name__ == "__main__":
	dirCreate()
	data = Data("datasets/dataset_train.csv")

	fig, axs = plt.subplots()

	axs.set(xlabel='Defense Against the Dark Arts', ylabel='Astronomy')

	x_data = data.allHouses['Defense Against the Dark Arts']
	y_data = data.allHouses['Astronomy']

	axs.scatter(x_data, y_data)

	fig.savefig("Visualization/scatter_plot.png")