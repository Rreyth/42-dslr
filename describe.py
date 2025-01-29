from sys import argv, stderr
from classes.Data import Data

if len(argv) != 2:
	print("Error: wrong number of arguments", file=stderr)
	print("Usage: python describe.py <dataset>.csv")
	exit(1)

if not argv[1].endswith(".csv"):
	print("Error: argument must be a csv file", file=stderr)
	print("Usage: python describe.py <dataset>.csv")
	exit(1)

data = Data(argv[1])
data.describe()
