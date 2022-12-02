import numpy as np
from Encoder.stage import stage1 as st1, stage2 as st2


def d_lsf(codeword):
    """
    Определение вектора квантованных ЛСЧ
    :param codeword: индексы вектора ЛСЧ в 4-х КК
    :return:
    f - вектор квантованных ЛСЧ
    """
    temp = np.zeros((4, 10))
    temp[0, :] = st1[int((codeword[0] - 1) * 10):int(codeword[0] * 10)]
    temp[1, :] = st2[0, int((codeword[1] - 1) * 10): int(codeword[1] * 10)]
    temp[2, :] = st2[1, int((codeword[2] - 1) * 10): int(codeword[2] * 10)]
    temp[3, :] = st2[2, int((codeword[3] - 1) * 10): int(codeword[3] * 10)]
    return sum(temp)
