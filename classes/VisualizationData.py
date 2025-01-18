from sys import stderr
from collections import defaultdict

class VisualizationData:
	def __init__(self, filepath: str) -> None:
		self.houses = defaultdict(lambda: defaultdict(list))

		try:
			file = open(filepath)
		except Exception as e:
			print(f"Error: {e}", file=stderr)
			exit(1)
		content = [line.split(",") for line in file.read().splitlines()]
		names = content.pop(0)

		for i in range(1, len(content)):
			house = content[i][1]

			for j in range(6, len(content[i])):
				if (content[i][j] != ""):
					self.houses[house][names[j]].append(float(content[i][j]))
