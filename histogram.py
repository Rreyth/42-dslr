import matplotlib.pyplot as plt

from classes.VisualizationData import VisualizationData

def set_hist(plot, title, data):
    plot.hist(data, label=title, alpha=.5, edgecolor='red')
    plot.set_title(title)

data = VisualizationData("datasets/dataset_train.csv")

fig, axs = plt.subplots(nrows=4, ncols=4, figsize=(15,15))

courses = data.houses["Gryffindor"].keys()
houses = data.houses.keys()

cols_count = 4

for i, course in enumerate(courses):
    for house in houses:
        axs[int(i / cols_count), i % cols_count].hist(data.houses[house][course], bins=100, alpha=0.5, label=house)
        axs[int(i / cols_count), i % cols_count].set_title(course)

fig.delaxes(axs[3, 1])
fig.delaxes(axs[3, 2])
fig.delaxes(axs[3, 3])

for ax in axs.flat:
    ax.set(xlabel='Grades', ylabel='Count')

fig.tight_layout(pad=4.0)

handles, labels = axs[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower right', fontsize="20", bbox_to_anchor=(0.96, 0.04))

fig.savefig("histogram.png")
