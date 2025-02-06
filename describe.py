import argparse
from classes.Data import Data
from functions.file_utils import IsCSVFile


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset", action=IsCSVFile, help="path to the dataset file")

	args = parser.parse_args()

	data = Data(args.dataset)
	data.describe()


if __name__ == "__main__":
	main()
