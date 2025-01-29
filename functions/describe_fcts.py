import numpy as np

def ft_mean(values : list) -> float:
	res = 0
	for val in values:
		if np.isnan(val):
			continue
		res += val
	res /= len(values)
	return res

def ft_std(values : list) -> float:
	mean = ft_mean(values)
	res = 0
	for val in values:
		if np.isnan(val):
			continue
		res += (val - mean) ** 2
	res = res ** 0.5
	return res

def ft_min(values : list) -> float:
	res = values[0] if values[0] != np.nan else 9999999
	for val in values:
		if np.isnan(val):
			continue
		if val < res:
			res = val
	return res

def ft_percentile(values : list, percentile):
	cpy = [x for x in values if not np.isnan(x)]
	cpy.sort()
	n = len(cpy)
	idx = round(percentile * (n + 1) / 100) - 1
	return cpy[idx]

def ft_max(values : list) -> float:
	res = values[0] if values[0] != np.nan else -9999999
	for val in values:
		if np.isnan(val):
			continue
		if val > res:
			res = val
	return res

def to_dict(names : list, line : list) -> dict:
	res = {}
	for i in range(len(line)):
		res[names[i]] = line[i]
		
	return res
