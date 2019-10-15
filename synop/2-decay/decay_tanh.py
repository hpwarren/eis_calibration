import numpy as np

def decay_tanh(t, a, b, c):
    return a*(1 + b*np.tanh(c*t))
