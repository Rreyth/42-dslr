from classes.VisualizationData import VisualizationData

if __name__ == "__main__":
    data = VisualizationData("datasets/dataset_train.csv")

    courses = data.houses["Gryffindor"].keys()
    houses = data.houses.keys()

    courses_count = len(courses)

    fig, axs = plt.subplots(nrows=courses_count, ncols=courses_count, figsize=(15,15))

    for house in houses:
        data.houses["all_houses"]

    for y, course_y in enumerate(courses):
        for x, course_x in enumerate(courses):
            if (course_y != course_x):
                axs[y, x].scatter(data.houses[house][course_y], bins=100, alpha=0.5)
                axs[y, x].scatter(data.houses[house][course_x], bins=100, alpha=0.5)
            else:
                for house in houses:
                    axs[y, x].hist(data.houses[house][course], bins=100, alpha=0.5, label=house)

    for i, course in enumerate(courses):
        for house in houses:
            axs[int(i / cols_count), i % cols_count].hist(data.houses[house][course], bins=100, alpha=0.5, label=house)
            axs[int(i / cols_count), i % cols_count].set_title(course)
