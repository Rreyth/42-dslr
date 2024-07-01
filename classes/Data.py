from functions.describe_fcts import *

class Data:
	def __init__(self, content : list[dict]):
		self.content = content
		self.name_list = []
		self.count_list = []
		self.mean_list = []
		self.std_list = []
		self.min_list = []
		self.quarter_list = []
		self.mid_list = []
		self.three_quarter_list = []
		self.max_list = []
		
		self.columnCalc()

	def columnCalc(self):
		for key, value in self.content[0].items():
			if key == 'Index':
				continue
			try:
				float(value)
				column = self.makeColumn(key)
				self.name_list.append(key)
				self.mean_list.append(ft_mean(column))
				self.std_list.append(ft_std(column))
				self.min_list.append(ft_min(column))
				self.quarter_list.append(ft_percentile(column, 25))
				self.mid_list.append(ft_percentile(column, 50))
				self.three_quarter_list.append(ft_percentile(column, 75))
				self.max_list.append(ft_max(column))
			except Exception:
				continue

	def makeColumn(self, key):
		column = []
		count = 0
		for entry in self.content:
			try:
				column.append(float(entry[key]))
				count += 1
			except Exception:
				continue

		self.count_list.append(count)
		return column

	def describe(self):
		text = "\t"
		for i in range(len(self.name_list)):
			name = self.name_list[i].split()
			name = name[0] if len(name) > 1 else self.name_list[i]
			if len(name) <= 8:
				name += "\t"
			text += name
			if i != len(self.name_list) - 1:
				text += "\t"
		text += "\nCount\t"
		for i in range(len(self.count_list)):
			text += str(self.count_list[i])
			if i != len(self.count_list) - 1:
				text += "\t\t"
		text += "\nMean\t"
		for i in range(len(self.mean_list)):
			text += f"{self.mean_list[i]:.6f}"
			if i != len(self.mean_list) - 1:
				text += "\t"
		text += "\nStd\t"
		for i in range(len(self.std_list)):
			text += f"{self.std_list[i]:.6f}"
			if i != len(self.std_list) - 1:
				text += "\t"
		text += "\nMin\t"
		for i in range(len(self.min_list)):
			text += f"{self.min_list[i]:.6f}"
			if i != len(self.min_list) - 1:
				text += "\t"
		text += "\n25%\t"
		for i in range(len(self.quarter_list)):
			text += f"{self.quarter_list[i]:.6f}"
			if i != len(self.quarter_list) - 1:
				text += "\t"
		text += "\n50%\t"
		for i in range(len(self.mid_list)):
			text += f"{self.mid_list[i]:.6f}"
			if i != len(self.mid_list) - 1:
				text += "\t"
		text += "\n75%\t"
		for i in range(len(self.three_quarter_list)):
			text += f"{self.three_quarter_list[i]:.6f}"
			if i != len(self.three_quarter_list) - 1:
				text += "\t"
		text += "\nMax\t"
		for i in range(len(self.max_list)):
			text += f"{self.max_list[i]:.6f}"
			if i != len(self.max_list) - 1:
				text += "\t"
		print(text)