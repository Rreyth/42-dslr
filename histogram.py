import matplotlib.pyplot as plt
from functions.describe_fcts import ft_mean, ft_std

from classes.VisualizationData import VisualizationData

def most_homogeneous_course_histogram(data: VisualizationData, most_homogeneous_course):
    fig, axs = plt.subplots()

    for house in houses:
        axs.hist(data.houses[house][most_homogeneous_course], bins=100, alpha=0.5, label=house)

    axs.set_title(most_homogeneous_course)
    axs.set(xlabel='Marks', ylabel='Count')
    handles, labels = axs.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right', framealpha=1.0, bbox_to_anchor=(0.9, 0.88))

    fig.savefig("histogram.png")

def all_courses_histogram(data: VisualizationData, courses, houses):
    fig, axs = plt.subplots(nrows=4, ncols=4, figsize=(15,15))

    cols_count = 4

    for i, course in enumerate(courses):
        for house in houses:
            axs[int(i / cols_count), i % cols_count].hist(data.houses[house][course], bins=100, alpha=0.5, label=house)
            axs[int(i / cols_count), i % cols_count].set_title(course)

    for i in range(1, 4):
        fig.delaxes(axs[3, i])

    for ax in axs.flat:
        ax.set(xlabel='Marks', ylabel='Count')

    fig.tight_layout(pad=4.0)

    handles, labels = axs[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower right', fontsize="20", bbox_to_anchor=(0.96, 0.04))

    fig.savefig("all_courses_histogram.png")

def courses_std_dev_bar_plot(courses_std_dev: dict):
    fig, axs = plt.subplots(figsize=(15,5))

    courses_std_dev = dict(sorted(courses_std_dev.items(), key=lambda x: x[1]))

    axs.bar(courses_std_dev.keys(), courses_std_dev.values())
    fig.tight_layout(pad=4.0)

    x = range(len(courses_std_dev.keys()))
    plt.xticks(x, courses_std_dev.keys(), rotation=45)

    fig.subplots_adjust(bottom=0.375)
    axs.set(xlabel='Courses', ylabel='Std. Dev.')

    fig.savefig("bar_plot.png")

if __name__ == "__main__":
    data = VisualizationData("datasets/dataset_train.csv")

    courses = data.houses["Gryffindor"].keys()
    houses = data.houses.keys()
    courses_std_dev = dict()
    courses_mean = list()

    for i, course in enumerate(courses):

        course_min = min([min(data.houses[house][course]) for house in houses])
        course_max = max([max(data.houses[house][course]) for house in houses])

        for house in houses:
            normed = [(float(i) - course_min) / (course_max - course_min) for i in data.houses[house][course]]
            courses_mean.append(ft_mean(normed))

        courses_std_dev[course] = ft_std(courses_mean)
        courses_mean.clear()

    most_homogeneous_course = min(courses_std_dev, key=courses_std_dev.get)
    most_homogeneous_course_histogram(data, most_homogeneous_course)
    all_courses_histogram(data, courses, houses)
    courses_std_dev_bar_plot(courses_std_dev)
