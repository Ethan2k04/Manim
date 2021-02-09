import numpy as np

def cos_n_times(x,n=10):
    for i in range(n):
        x = np.cos(x)
    return x

print(cos_n_times(10,100))