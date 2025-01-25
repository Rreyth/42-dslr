from os import path, makedirs
from sys import stderr
import matplotlib.pyplot as plt
from classes.VisualizationData import VisualizationData

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
	data = VisualizationData("datasets/dataset_train.csv")

	courses = data.houses["Gryffindor"].keys()
	houses = data.houses.keys()

	courses_count = len(courses)

	fig, axs = plt.subplots(nrows=courses_count, ncols=courses_count, figsize=(40,40))

	for y, course_y in enumerate(courses):
		title = course_y
		title_y = 0.4
		if course_y == 'Defense Against the Dark Arts':
			title = 'Defense Against\nthe Dark Arts'
			title_y = 0.35
		elif course_y == 'Care of Magical Creatures':
			title = 'Care of\nMagical Creatures'
			title_y = 0.35
		axs[y, 0].set(ylabel=title)
		axs[0, y].set(xlabel=title)
		axs[0, y].xaxis.set_label_position('top')
		axs[0, y].xaxis.label.set_size(20)
		axs[y, 0].yaxis.label.set_size(20)
		for x, course_x in enumerate(courses):
			if course_y != course_x:
				x_data = data.allHouses[course_x]
				y_data = data.allHouses[course_y]

				axs[y, x].scatter(x_data, y_data)
				axs[y, x].label_outer(remove_inner_ticks=True)

			else:
				for house in houses:
					axs[y, x].hist(data.houses[house][course_x], bins=100, alpha=0.5, label=house)
					axs[y, x].label_outer(remove_inner_ticks=True)

	fig.savefig("Visualization/pair_plot.png")
