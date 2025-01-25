import math as m

def list_exp(values):
	res = []
	for value in values:
		res.append(m.exp(value))
	return res

def list_abs(values):
	res = []
	for value in values:
		res.append(value if value >= 0 else -value)
	return res
