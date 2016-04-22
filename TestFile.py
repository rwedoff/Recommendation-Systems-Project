# Movie Recommendation Systems
# Ryan Wedoff & Zongsheng Sun
# Data From http://grouplens.org/datasets/movielens/

import numpy as np
from RecommendationFile import *

#recommend('ml-1m/ratings.dat')

# Run SVD
# Used for ml-100k only
recommend('ml-100k/u1.base')

# calculate the Mean Square Error
svd_result = np.load("svd_result-100k.dat")
f = open('ml-100k/u1.test', 'r', encoding='utf-8')
Error_Square_Sum = 0
count = 0
for line in f:
    chunk = line.split("\t")
    Error_Square_Sum += (svd_result[int(chunk[0]) - 1, int(chunk[1]) - 1] - int(chunk[2])) ** 2
    count += 1
f.close()
MSE = (Error_Square_Sum / (count - 1)) ** 0.5
print(MSE)
