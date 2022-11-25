import numpy as np


def melp_lsf21pc(lsfs):
    """
    Конвертер LSF в LPC
    :param lsfs: ЛСЧ
    :return: f - Коэффициенты ЛП
    """

    global tmp1, tmp2, tmp3, tmp4
    Q = np.zeros((2, 11))
    w = np.zeros((2, 5))
    lsfs = np.pi * lsfs / 4000
    for i in np.arange(5):
        for j in np.arange(2):
            w[j, i] = lsfs[i * 2 + j]

    w = np.cos(w)
    for i in np.arange(2):
        temp = np.array([1, - 2 * w[i, 4], 1])
        P = temp
        for j in np.arange(4):
            temp = np.asarray([1, - 2 * w[i, j], 1])
            tmp1 = np.append(P, (0, 0))
            tmp2_1 = np.append(0, P)
            tmp2 = np.append(tmp2_1, 0)
            tmp3 = np.append((0, 0), P)
            w0 = np.vstack((tmp1, tmp2, tmp3))
            P = np.matmul(temp, w0)

        Q[i, :] = P
    tmp1 = np.append(Q[0, :], 0)
    tmp3 = np.append(0, Q[0, :])
    tmp2 = np.append(Q[1, :], 0)
    tmp4 = np.append(0, Q[1, :])
    f = (tmp1 + tmp2 + tmp3 - tmp4) / 2
    f = f[1:11]
    return f
