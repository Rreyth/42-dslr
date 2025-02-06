import argparse
from sys import stderr
from os import path, makedirs


def dir_create(name : str):
	if path.isdir(name):
		return
	try:
		makedirs(name)
	except Exception as e:
		print(f"Error: {e}", file=stderr)
		exit(1)


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


def make_houses(filepath):
	try:
		file = open(filepath)
	except Exception as e:
		print(f"Error: {e}", file=stderr)
		exit(1)
	content = [line.split(",") for line in file.read().splitlines()]
	houses = [{'name': content.pop(0)[0], 'weights': content.pop(0)},
	          {'name': content.pop(0)[0], 'weights': content.pop(0)},
	          {'name': content.pop(0)[0], 'weights': content.pop(0)},
	          {'name': content.pop(0)[0], 'weights': content.pop(0)}]

	return houses


def save_weights(save):
	file = False
	try:
		file = open("weights", 'x+t')
	except Exception as e:
		try:
			file = open("weights", 'w+t')
		except Exception as e:
			print(f"Error: {e}", file=stderr)
			exit(1)

	file.write(save)


class IsCSVFile(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		if not values.endswith(".csv"):
			raise argparse.ArgumentError(self, f"'{values}' is not a csv file.")
		setattr(namespace, self.dest, values)
