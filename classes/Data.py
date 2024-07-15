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
		text = "\t" + _format_names(self.name_list)
		text += "\nCount\t" + _format_values(self.count_list)
		text += "\nMean\t" + _format_values(self.mean_list)
		text += "\nStd\t" + _format_values(self.std_list)
		text += "\nMin\t" + _format_values(self.min_list)
		text += "\n25%\t" + _format_values(self.quarter_list)
		text += "\n50%\t" + _format_values(self.mid_list)
		text += "\n75%\t" + _format_values(self.three_quarter_list)
		text += "\nMax\t" + _format_values(self.max_list)
		print(text)


def _format_names(names : list):
	res = ""
	for i, name in enumerate(names):
		first_word = name.split()[0]
		res += first_word
		res += "\t" if len(first_word) < 8 else ""
		res += "\t" if i != len(names) - 1 else ""
	return res

def _format_values(values : list):
	res = ""
	for i, value in enumerate(values):
		formated_value = f"{value:.6f}" if isinstance(value, float) else f"{value}"
		dot_pos = formated_value.find(".")
		if dot_pos != -1:
			while formated_value[len(formated_value) - 1] == "0" and formated_value[len(formated_value) - 2] != '.':
				formated_value = formated_value[:-1]
		res += formated_value + ("\t" if len(formated_value) < 8 else "")
		res += "\t" if i != len(values) - 1 else ""
	return res
