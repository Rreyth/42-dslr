from sys import argv, stderr
from classes.Data import Data


if len(argv) != 2:
	print("Error: wrong number of arguments", file=stderr)
	print("Usage: describe.py <dataset>.csv")
	exit(1)

if not argv[1].endswith(".csv"):
	print("Error: argument must be a csv file", file=stderr)
	print("Usage: describe.py <dataset>.csv")
	exit(1)


def to_dict(names : list, line : list) -> dict:
    res = {}
    for i in range(len(line)):
        res[names[i]] = line[i]
        
    return res


try:
	dataset = open(argv[1], 'r')
	content = [line.split(",") for line in dataset.read().splitlines()]
	names = content.pop(0)
	for i in range(len(content)):
		content[i] = to_dict(names, content[i])

	data = Data(content)
	data.describe()

except Exception as e:
	print(e, file=stderr)
