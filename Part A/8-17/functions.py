import numpy as np
from scipy.stats import entropy


#function responsible for computing the motion vector via logarithmic search, initialized with K = 16.
def compute_motion_vector(macroblock, ref, coordinates):
    K=16 #initialize search parameter equal to 16.
    p = [0, K/2, -K/2]
    best = sad(macroblock, ref[coordinates[0]:coordinates[0] + 16, coordinates[1]:coordinates[1] + 16]) #implements sad algorithm - method.
    bestcoordinates = coordinates
    while True:
        for i in range(len(p)):
            for j in range(len(p)):
                if p[i] == p[j] == 0:
                    continue
                try:
                    temp = sad(macroblock, ref[int(bestcoordinates[0] + p[i]):int(bestcoordinates[0] + 16 + p[i]), int(bestcoordinates[1] + p[j]):int(bestcoordinates[1] + 16 + p[j])])
                    if temp < best:
                        best = temp
                        bestcoordinates = (bestcoordinates[0] + p[i], bestcoordinates[1] + p[j])
                except IndexError:
                    pass
        p[:] = [x / 2 for x in p] #new step's size decreased to it's half.
        if p[1] < 1:
            break
    return tuple(np.subtract(bestcoordinates, coordinates, dtype=int, casting='unsafe'))


#function responsible for calculating the Sum Absolute Difference(S.A.D.).
def sad(first, second):
    sad = 0 #initialize sad equalto 0.
    r = first.shape[0] #number of rows.
    for i in range(r):
        for j in range(r):
			#S.A.D. is the sum of the absolute difference between the two frames
            sad += abs(int(first[i, j]) - int(second[i, j]))
    return sad


#function responsible for the Entropy Calculation(Helped by scipy.stats library).
def entropy_calculation(labels, base=None):
  _,counts = np.unique(labels, return_counts=True)
  return entropy(counts, base=base)
