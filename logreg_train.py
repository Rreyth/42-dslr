import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np

data = np.array([[5, 0], [10, 0], [15, 1], [20, 1]])

plt.scatter(x=np.take(data, [0], 1), y=np.take(data, [1], 1))
plt.show()

