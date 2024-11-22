import matplotlib as mpl
import matplotlib.pyplot as plt
import statistics

from classes.VisualizationData import VisualizationData

def set_hist(plot, title, data):
    plot.hist(data, label=title, alpha=.5, edgecolor='red')
    plot.set_title(title)

def norm(list: list):
    return [(float(i) - min(list)) / (max(list) - min(list)) for i in list]

data = VisualizationData("datasets/dataset_train.csv")

courses = data.houses["Gryffindor"].keys()
houses = data.houses.keys()

# fig, axs = plt.subplots(nrows=4, ncols=4, figsize=(15,15))

# cols_count = 4

# for i, course in enumerate(courses):
#     for house in houses:
#         axs[int(i / cols_count), i % cols_count].hist(data.houses[house][course], bins=100, alpha=0.5, label=house)
#         axs[int(i / cols_count), i % cols_count].set_title(course)

# fig.delaxes(axs[3, 1])
# fig.delaxes(axs[3, 2])
# fig.delaxes(axs[3, 3])

# for ax in axs.flat:
#     ax.set(xlabel='Grades', ylabel='Count')

# fig.tight_layout(pad=4.0)

# handles, labels = axs[0, 0].get_legend_handles_labels()
# fig.legend(handles, labels, loc='lower right', fontsize="20", bbox_to_anchor=(0.96, 0.04))

# fig.savefig("histogram.png")







courses_std_dev = list()
courses_mean = list()

for i, course in enumerate(courses):

    course_min = min([min(data.houses[house][course]) for house in houses])
    course_max = max([max(data.houses[house][course]) for house in houses])

    for house in houses:
        normed = [(float(i) - course_min) / (course_max - course_min) for i in data.houses[house][course]]
        courses_mean.append(statistics.mean(normed))
    
    courses_std_dev.append(statistics.stdev(courses_mean))
    courses_mean.clear()

fig, axs = plt.subplots(figsize=(15,5))

# cols_count = 4

# for i, course in enumerate(courses):
#     for house in houses:
#         axs[int(i / cols_count), i % cols_count].hist(data.houses[house][course], bins=100, alpha=0.5, label=house)
#         axs[int(i / cols_count), i % cols_count].set_title(course)

# fig.delaxes(axs[3, 1])
# fig.delaxes(axs[3, 2])
# fig.delaxes(axs[3, 3])

# for ax in axs.flat:
#     ax.set(xlabel='Grades', ylabel='Count')

axs.bar(courses, courses_std_dev)
# axs.hist(courses_std_dev)
fig.tight_layout(pad=4.0)

x = range(len(courses))
plt.xticks(x, courses, rotation=45)

fig.subplots_adjust(bottom=0.375)
axs.set(xlabel='Courses', ylabel='Std. Dev.')


# handles, labels = axs[0, 0].get_legend_handles_labels()
# fig.legend(handles, labels, loc='lower right', fontsize="20", bbox_to_anchor=(0.96, 0.04))

fig.savefig("histogram2.png")