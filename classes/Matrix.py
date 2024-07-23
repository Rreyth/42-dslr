class Matrix:
	def __init__(self, elements : list[list[int | float]]):
		size = elements[0].__len__()
		for line in elements:
			if line.__len__() != size:
				raise ValueError("Matrix must be a rectangle or a square")
			for elem in line:
				if not isinstance(elem, (int, float)):
					raise TypeError("Matrix argument must be a list of lists of [int or float]")
		self.elems = elements

	def size(self):
		size = [self.elems.__len__(), self.elems[0].__len__()]
		return size

	def __str__(self):
		ret = ""
		for i, line in enumerate(self.elems):
			ret += str(line)
			if i != self.elems.__len__() - 1:
				ret += "\n"
		return ret

	def __getitem__(self, keys):
		r, c = keys
		return self.elems[r][c]

	def __setitem__(self, keys, value):
		if not isinstance(value, (int, float)):
			raise TypeError("Matrix only contains int or float types")
		r, c = keys
		self.elems[r][c] = value

	def __mul__(self, scalar : int | float):
		if not isinstance(scalar, (int, float)):
			raise TypeError("Scalar must be of type int or float")

		res = []
		for i in range(self.size()[0]):
			res.append([])
			for j in range(self.size()[1]):
				res[i].append(self.elems[i][j] * scalar)
    
		return Matrix(res)

	def scale(self, scalar : int | float):
		if not isinstance(scalar, (int, float)):
			raise TypeError("Scalar must be of type int or float")
		for i in range(self.size()[0]):
			for j in range(self.size()[1]):
				self.elems[i][j] *= scalar

	def isSquare(self):
		return self.elems.__len__() == self.elems[0].__len__()

	def transpose(self):
		res = []
		for i in range(self.size()[1]):
			res.append([])
			for j in range(self.size()[0]):
				res[i].append(self[j, i])
    
		return Matrix(res)

	def dot(self, elem):
		if isinstance(elem, Matrix):
			if self.size()[1] != elem.size()[0]:
				raise ValueError("Second Matrix must have a number of line equal to first Matrix number of columns")
			res = []
			for i in range(self.size()[0]):
				res.append([])
				for j in range(elem.size()[1]):
					res[i].append(0)
					for k in range(elem.size()[0]):
						res[i][j] += self[i, k] * elem[k, j]

			return Matrix(res)

		else:
			if self.size()[1] != len(elem):
				raise ValueError("list must have a size equal to Matrix number of columns")
			res = []
			for i in range(self.size()[0]):
				res.append(0)
				for j in range(self.size()[1]):
					res[i] += self.elems[i][j] * elem[j]

			return res

	def subMatrix(self, row, column):
		mat = []
		for i in range(self.size()[0]):
			if i == row:
				continue
			line = []
			for j in range(self.size()[1]):
				if j == column:
					continue
				line.append(self[i, j])
			mat.append(line)
		return Matrix(mat)

	def colToLine(self, column):
		if not 0 <= column <= self.size()[1] or not isinstance(column, int):
			raise ValueError("number must be an int between 0 and matrix size included")
		res = []
		for i in range(self.size()[0]):
			res.append(self[i, column])
   
		return res

	def addCol(self, new_column : list):
		for i in range(self.size()[0]):
			self.elems[i].append(new_column[i])
