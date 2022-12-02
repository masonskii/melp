def melp_lpc2lsf(a):
    """
    Конвертирует коэффициенты ЛП в ЛСЧ
    :param a: параметр ЛП
    :return: f - параметр ЛСЧ

    :NOTES:
    В даной функции все параметры полиномов выстроены по возрастанию
    """
    try:
        import numpy as np

        global temp
        P = np.zeros((2, 6))
        P[0, 0], P[1, 0] = 1, 1
        for i in np.arange(5):
            P[0, i + 1] = a[i] + a[10 - (i + 1)] - P[0, i]
            P[1, i + 1] = a[i] - a[10 - (i + 1)] + P[1, i]

        P[:, 5] = P[:, 5] / 2
        P = np.fliplr(P)

        b = np.zeros((6, 6))
        b[0, 0] = 1
        b[1, 1] = 1
        for i in np.arange(4):
            tmp1 = b[i + 1, 0:i + 1 + 1]
            tmp1 = np.append([0], tmp1)
            tmp2 = np.append(b[i, 0:i + 1], [0, 0])
            b[i + 2, 0:i + 2 + 1] = 2 * tmp1 - tmp2

        P = np.matmul(P, b)
        f1 = [0]

        for ii in np.arange(2):
            k = np.pi / 60
            y1 = np.sum(P[ii, :])
            i = 1
            while i < 61:
                cosx = np.cos(i * k)
                y2 = np.matmul(np.power(cosx, np.arange(1, 6, 1)), np.reshape(P[ii, 1:6], (-1, 1))) + P[ii, 0]
                if y2 == 0:
                    f1.append(i * k)
                    i += 1
                    cosx = np.cos(i * k)
                    y2 = np.matmul(np.power(cosx, np.arange(1, 6, 1)), np.reshape(P[ii, 1:6], (-1, 1))) + P[ii, 0]
                elif y1 * y2 < 0:
                    x1 = (i - 1) * k
                    x2 = i * k
                    for _ in np.arange(4):
                        x = (x1 + x2) / 2
                        cosx = np.cos(x)
                        temp = np.matmul(np.power(cosx, np.arange(1, 6)), np.reshape(P[ii, 1:6], (-1, 1))) + P[ii, 0]
                        if temp == 0:
                            f1.append(x)
                            break
                        elif temp * y2 < 0:
                            x1 = x
                        else:
                            x2 = x
                            y2 = temp

                    if temp != 0:
                        f1.append((x1 + x2) / 2)
                y1 = y2
                i += 1
        f = np.zeros(10)
        m = len(f1)
        if m == 11:
            f[0] = f1[1]
            f[np.arange(1, 5) * 2] = f1[2:6]
            f[np.arange(1, 6) * 2 - 1] = f1[6:11]

        return f
    except Exception as e:
        raise e
