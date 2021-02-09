import numpy as np
def basel(n=1000):
    sum = 0
    start = 1
    for i in range(n):
        sum += 1/start**2
        start += 1
    return sum

print("近似计算结果:",basel())

def second_question(n=10000):
    last = n + 1
    for i in range(n):
        last = 1 + n*np.sqrt(last)
        n -= 1
    return last
print(second_question())