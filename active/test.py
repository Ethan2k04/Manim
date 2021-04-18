import numpy as np
for v in range(15):
    v *= 10
    print(100 * np.power(300, -3/2) * v ** 2 * np.exp(-0.1 * v**2 / 300))

print(np.power(1, -3/2))