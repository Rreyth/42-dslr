from sys import stderr
from collections import defaultdict
from functions.describe_fcts import *

class Data:
	def __init__(self, filepath: str):
		self.houses = defaultdict(lambda: defaultdict(list))
		self.allHouses = defaultdict(list)
		self.studs = []
		self.name_list = []
		self.count_list = []
		self.mean_list = []
		self.std_list = []
		self.min_list = []
		self.quarter_list = []
		self.mid_list = []
		self.three_quarter_list = []
		self.max_list = []
		self.iqr_list = []
		self.range_list = []
		self.skew_list = []
		self.kurt_list = []
		self.var_list = []

		try:
			file = open(filepath)
		except Exception as e:
			print(f"Error: {e}", file=stderr)
			exit(1)
		content = [line.split(",") for line in file.read().splitlines()]
		names = content.pop(0)
		for i in range(len(content)):
			self.studs.append(to_dict(names, content[i]))
			house = content[i][1]
			for j in range(6, len(content[i])):
				if content[i][j] != '':
					self.houses[house][names[j]].append(float(content[i][j]))
					self.allHouses[names[j]].append(float(content[i][j]))
				else:
					self.allHouses[names[j]].append(np.nan)

		self.column_calc()

	def __str__(self) -> str:
		res = ""
		for stud in self.studs:
			for name, value in stud.items():
				res += name + ": " + value + "\n"
			res += "-----------------------------------\n"
		return res

	def get_col(self, name):
		idx = self.name_list.index(name)
		res = {"count": self.count_list[idx],
		       "mean": self.mean_list[idx],
		       "std": self.std_list[idx],
		       "min": self.min_list[idx],
		       "25": self.quarter_list[idx],
		       "50": self.mid_list[idx],
		       "75": self.three_quarter_list[idx],
		       "max": self.max_list[idx],
		       "iqr": self.iqr_list[idx],
		       "range": self.range_list[idx],
		       "skew": self.skew_list[idx],
		       "kurt": self.kurt_list[idx],
		       "var": self.var_list[idx]}
		return res

	def column_calc(self):
		for key, values in self.allHouses.items():
			self.count_list.append(len([x for x in values if not np.isnan(x)]))
			self.name_list.append(key)
			self.mean_list.append(ft_mean(values))
			self.std_list.append(ft_std(values))
			self.min_list.append(ft_min(values))
			self.quarter_list.append(ft_percentile(values, 25))
			self.mid_list.append(ft_percentile(values, 50))
			self.three_quarter_list.append(ft_percentile(values, 75))
			self.max_list.append(ft_max(values))
			self.iqr_list.append(ft_iqr(values))
			self.range_list.append(ft_max(values) - ft_min(values))
			self.skew_list.append(ft_skewness(values))
			self.kurt_list.append(ft_kurtosis(values))
			self.var_list.append(ft_variance(values))

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
		text += "\nIQR\t" + _format_values(self.iqr_list)
		text += "\nRange\t" + _format_values(self.range_list)
		text += "\nSkew\t" + _format_values(self.skew_list)
		text += "\nKurt\t" + _format_values(self.kurt_list)
		text += "\nVar\t" + _format_values(self.var_list)
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
		formated_value = f"{value:.2f}" if isinstance(value, float) else f"{value}"
		dot_pos = formated_value.find(".")
		if dot_pos != -1:
			while formated_value[len(formated_value) - 1] == "0" and formated_value[len(formated_value) - 2] != '.':
				formated_value = formated_value[:-1]
		res += formated_value + ("\t" if len(formated_value) < 8 else "")
		res += "\t" if i != len(values) - 1 else ""
	return res
