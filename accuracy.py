from sys import stderr
from sklearn.metrics import accuracy_score


def open_house_file(name):
	try:
		file = open(name)
	except Exception as e:
		print(f"Error: {e}", file=stderr)
		exit(1)
	content = [line.split(",") for line in file.read().splitlines()]
	content.pop(0)

	houses = [house for i, house in content]

	return houses


def main():
	pred = open_house_file('houses.csv')
	real = open_house_file('real_houses.csv')

	print(accuracy_score(real, pred))


if __name__ == "__main__":
	main()
