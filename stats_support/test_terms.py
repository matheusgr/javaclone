import distribution

vals = list(map(float, open("data.txt").readlines()))

best_dist, best_p, params = distribution.get_best_distribution(vals)

from scipy.stats import genextreme
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(1, 1)

c, loc, scale = params
fit_mean= loc
min_extreme,max_extreme = genextreme.interval(0.90,c,loc,scale) 
print(min_extreme,max_extreme)

# evenly spread x axis values for pdf plot
x = np.linspace(min(vals),max(vals),200)

# plot distribution
plt.plot(x, genextreme.pdf(x, *genextreme.fit(x)))
plt.hist(vals,30,alpha=0.3)
plt.show()