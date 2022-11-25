def convert(argc, argv='m'):
    if argv == 'p':
        return argc + 1
    if argv == 'm':
        return argc - 1


def d_k1(p):
    try:
        import numpy as np
        k = -p[convert(10)]
        pp = np.zeros(convert(p.size))
        for n in np.arange(1, 10):
            j = 11 - n
            for i in np.arange(1, j):
                pp[convert(i)] = (p[convert(i)] - (k * p[convert(j - i)])) / (1 - (k ** 2))
            p = np.copy(pp)
            k = -p[convert(j - 1)]
        return k
    except Exception as e:
        raise e
