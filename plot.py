# install matplotlib: https://matplotlib.org/stable/users/getting_started/index.html
# source: https://stackoverflow.com/questions/38532298/how-can-you-plot-data-from-a-txt-file-using-matplotlib

import numpy  as np
import matplotlib.pyplot as plt
data = np.loadtxt('input.txt')

x = data[:]
plt.plot(x)
plt.show()