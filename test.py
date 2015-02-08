import numpy as np
#dmax = 10
#
#arr = [0, 1, 0, 1, 0, 0, 0, 1, 0, 0]

def autocorrelation(arr, dmax):                                
    acorr = np.zeros(dmax)
    for d in range(1,min(dmax,arr.shape[0])):
        acorr[d]+=np.sum(arr[d:] * arr[:-d])
     
    return acorr