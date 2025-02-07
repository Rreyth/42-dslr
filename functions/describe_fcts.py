import numpy as np

def ft_sum(values):
	res = 0
	for x in values:
		res += x
	return res

def ft_mean(values : list) -> float:
	cpy = [x for x in values if not np.isnan(x)]
	res = ft_sum(x for x in cpy) / len(cpy)

	return res

def ft_std(values : list) -> float:
	var = ft_variance(values)
	return var ** 0.5

def ft_min(values : list) -> float:
	cpy = [x for x in values if not np.isnan(x)]
	cpy.sort()
	return cpy[0]

def ft_percentile(values : list, percentile):
	cpy = [x for x in values if not np.isnan(x)]
	cpy.sort()
	n = len(cpy)
	idx = (percentile / 100) * (n - 1)
	if idx % 1 != 0 and idx < n - 1:
		weight = idx - int(idx)
		idx = int(idx)
		return cpy[idx] * (1 - weight) + cpy[idx + 1] * weight
	idx = int(idx)
	return cpy[idx]

def ft_max(values : list) -> float:
	cpy = [x for x in values if not np.isnan(x)]
	cpy.sort()
	return cpy[-1]

def ft_iqr(values : list) -> float:
	return ft_percentile(values, 75) - ft_percentile(values, 25)

def ft_skewness(values : list) -> float:
	cpy = [x for x in values if not np.isnan(x)]
	n = len(cpy)
	mean = ft_mean(values)
	std = (ft_sum((x - mean) ** 2 for x in cpy) / (n - 1)) ** 0.5

	p1 = n / ((n - 1) * (n - 2))
	p2 = ft_sum(((x - mean) / std) ** 3 for x in cpy)
	return p1 * p2

def ft_kurtosis(values : list) -> float:
	cpy = [x for x in values if not np.isnan(x)]
	n = len(cpy)
	mean = ft_mean(cpy)
	std = ft_std(cpy)

	kurtosis = ft_sum(((x - mean) / std) ** 4 for x in cpy)
	kurtosis /= n

	return kurtosis

def ft_variance(values : list) -> float:
	cpy = [x for x in values if not np.isnan(x)]
	mean = ft_mean(cpy)
	n = len(cpy)
	var = (1 / n) * ft_sum((x - mean) ** 2 for x in cpy)

	return var

def to_dict(names : list, line : list) -> dict:
	res = {}
	for i in range(len(line)):
		res[names[i]] = line[i]

	return res
