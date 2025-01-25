from sys import argv, stderr
from classes.Data import Data
from functions.describe_fcts import to_dict

if len(argv) != 2:
	print("Error: wrong number of arguments", file=stderr)
	print("Usage: python describe.py <dataset>.csv")
	exit(1)

if not argv[1].endswith(".csv"):
	print("Error: argument must be a csv file", file=stderr)
	print("Usage: python describe.py <dataset>.csv")
	exit(1)

try:
	dataset = open(argv[1], 'r')
	content = [line.split(",") for line in dataset.read().splitlines()]
	names = content.pop(0)
	for i in range(len(content)):
		content[i] = to_dict(names, content[i])

	data = Data(content)
	data.describe()

except Exception as e:
	print("Error:", e, file=stderr)
