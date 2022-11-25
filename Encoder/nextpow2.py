from numpy import ceil, log2


def nextpow2(x):
    res = ceil(log2(x))
    return res.astype('int')  # we want integer values only but ceil gives float
