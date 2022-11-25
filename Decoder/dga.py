import math


def d_ga(h, G, prev_scale, len):
    try:
        import numpy as np
        import cmath as cm
        scaleover = 10
        gain = np.power(10, 0.05 * G)
        scale = gain / (cm.sqrt(np.sum(np.power(h[:len], 2) / len) + 0.01)).real
        hh = np.zeros(len)
        for i in np.arange(0, scaleover - 1):
            hh[i] = h[i] * ((scale * (i+1) + prev_scale * (scaleover - (i+1))) * (1 / scaleover))

        hh[scaleover:len] = h[scaleover:len] / gain

        prev_scale = scale
        return hh, prev_scale
    except Exception as e:
        raise e
