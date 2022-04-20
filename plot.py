# install matplotlib: https://matplotlib.org/stable/users/getting_started/index.html
# source: https://stackoverflow.com/questions/38532298/how-can-you-plot-data-from-a-txt-file-using-matplotlib

import numpy  as np
import matplotlib.pyplot as plt
data = np.loadtxt('input.txt')
data2 = np.loadtxt('output.txt')

x = data[:]
x2 = data2[:]
plt.plot(x)
plt.plot(x2)
plt.show()
