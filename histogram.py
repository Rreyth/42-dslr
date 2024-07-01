import matplotlib.pyplot as plt
import numpy as np

def set_hist(plot, title, data):
    plot.hist(data, label=title, alpha=.5, edgecolor='red')
    plot.set_title(title)

fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2)

set_hist(ax0, 'house1', np.random.normal(170, 10, 250))
set_hist(ax1, 'house2', np.random.normal(170, 10, 250))
set_hist(ax2, 'house3', np.random.normal(170, 10, 250))
set_hist(ax3, 'house4', np.random.normal(170, 10, 250))

fig.tight_layout()
plt.show()