from copy import deepcopy

def ft_mean(values : list) -> float:
	res = 0
	for val in values:
		res += val
	res /= len(values)
	return res

def ft_std(values : list) -> float:
	mean = ft_mean(values)
	res = 0
	for val in values:
		res += (val - mean) ** 2
	res = res ** 0.5
	return res

def ft_min(values : list) -> float:
	res = values[0]
	for val in values:
		if val < res:
			res = val
	return res

def ft_percentile(values : list, percentile):
	cpy = deepcopy(values)
	cpy.sort()
	n = len(cpy)
	idx = round(percentile * (n + 1) / 100) - 1
	return cpy[idx]

def ft_max(values : list) -> float:
	res = values[0]
	for val in values:
		if val > res:
			res = val
	return res
