import numpy as np
import matplotlib.pyplot as plt
#def graphics(targets(), limits(), pads())

#plt.rcParams["figure.autolayout"] = True

data = np.array([[100, 170, 500, 666, 349],
   [10, 60, 200, 434, 777]])
point = data[:, 2]
ax = plt.gca()
ax.plot(data[0], data[1], 'o', ms=3, color='black')

#ax.set_xlim([2, 8])
#ax.set_ylim([0, 6])
radius = 10

ax.plot(point[0], point[1], 'o',
   ms=radius * 2, mec='red', mfc='none', mew=1)
#x1 = np.array([100, 170, 500, 666, 349])
#y1 = np.array([10, 60, 200, 434, 777])
R1 = np.array([1000, 2000, 3000, 4000, 5000])
P1 = np.array([10000, 15000, 40000, 60000, 100000])
targets = np.array([R1, P1])

plt.grid(visible = bool)
plt.show()
