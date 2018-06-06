from scipy.stats.kde import gaussian_kde
from numpy import linspace
import numpy as np
import matplotlib.pyplot as plt


f = open('output.txt')
data= np.loadtxt(f)
f.close()

# this create the kernel, given an array it will estimate the probability over that values
kde = gaussian_kde( data )

# these are the values over wich your kernel will be evaluated
dist_space = linspace( min(data), max(data), 100 )

# plot the results
plt.plot(dist_space, kde(dist_space) )
plt.show()