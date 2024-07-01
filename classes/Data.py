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
			text += self.name_list[i]
			if i != len(self.name_list) - 1:
				text += "\t"
		print(text)
		text = "Count\t"
		for i in range(len(self.count_list)):
			text += str(self.count_list[i])
			if i != len(self.count_list) - 1:
				text += "\t"
		print(text)
		text = "Mean\t"
		for i in range(len(self.mean_list)):
			text += str(self.mean_list[i])
			if i != len(self.mean_list) - 1:
				text += "\t"
		print(text)
		text = "Std\t"
		for i in range(len(self.std_list)):
			text += str(self.std_list[i])
			if i != len(self.std_list) - 1:
				text += "\t"
		print(text)
		text = "Min\t"
		for i in range(len(self.min_list)):
			text += str(self.min_list[i])
			if i != len(self.min_list) - 1:
				text += "\t"
		print(text)
		text = "25%\t"
		for i in range(len(self.quarter_list)):
			text += str(self.quarter_list[i])
			if i != len(self.quarter_list) - 1:
				text += "\t"
		print(text)
		text = "50%\t"
		for i in range(len(self.mid_list)):
			text += str(self.mid_list[i])
			if i != len(self.mid_list) - 1:
				text += "\t"
		print(text)
		text = "75%\t"
		for i in range(len(self.three_quarter_list)):
			text += str(self.three_quarter_list[i])
			if i != len(self.three_quarter_list) - 1:
				text += "\t"
		print(text)
		text = "Max\t"
		for i in range(len(self.max_list)):
			text += str(self.max_list[i])
			if i != len(self.max_list) - 1:
				text += "\t"
		print(text)