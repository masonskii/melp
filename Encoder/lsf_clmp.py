def lsf_clmp(LSF):
    """
    Регулирует расстояние между граничными ЛСЧ
    :param LSF: ЛСЧ
    :return:
    f - выровненные ЛСЧ
    """
    try:
        import numpy as np

        f = LSF * 4000 / np.pi
        dmin = 50
        for i in np.arange(9):
            d = f[i + 1] - f[i]
            if d < dmin:
                s1 = (dmin - d) / 2
                s2 = s1
                if i == 0 and (f[i] < dmin):
                    s1 = f[i] / 2
                elif i > 1:
                    temp = f[i] - f[i - 1]
                    if temp < dmin:
                        s1 = 0
                    elif temp < 2 * dmin:
                        s1 = (temp - dmin) / 2

                if i == 8 and (f[i + 1] > 4000 - dmin):
                    s2 = (4000 - f[i + 1]) / 2
                elif i < 8:
                    temp = f[i + 2] - f[i + 1]
                    if temp < dmin:
                        s2 = 0
                    elif temp < 2 * dmin:
                        s2 = (temp - dmin) / 2
                f[i] = f[i] - s1
                f[i + 1] = f[i + 1] + s2

        return f
    except Exception as e:
        raise e
