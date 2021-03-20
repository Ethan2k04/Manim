import numpy
import time

height = 60
t = 0
factor = 100
for h in range(height):
    print(" " * int(t) + "x" + "  " + str(h) + "m")
    t = numpy.sqrt(t**2 + factor)
    time.sleep(0.5)