import numpy as np

from Encoder.stage import stage1 as st1, stage2 as st2


def melp_msvq(lpcs, f):
    """
    Квантование коэффициентов линейного предсказания
    :param lpcs: коэффициенты ЛП
    :param f: соответствующие ЛСЧ
    :return:
        g - индекс в кодовой книге
    """
    try:
        w = np.zeros(10, dtype='complex_')
        for i in range(0, 10):
            a = np.exp(-1j * f[i] * np.arange(1, 11))
            b = np.reshape(lpcs, (-1, 1))
            w[i] = 1 + np.matmul(a, b)

        w = np.abs(w)
        w = np.power(w, 0.3)
        w[8] = w[8] * 0.64
        w[9] = w[9] * 0.16

        """
        % d(m,1)    - оценка 
        % d(m,2:11) - разность вектора и кодового слова
        % d(m,12:15)- кодовое слово 
        """
        d = np.zeros((9, 15))
        for l in range(np.shape(d)[0]):
            for ll in range(np.shape(d)[1]):
                d[l, ll] = 10000000
        # Определение индекса вектора КК первого уровня

        for i in range(0, 128):
            delta = f - st1[i * 10:(i + 1) * 10]
            temp = np.matmul(w, np.conj(np.transpose(np.power(delta, 2))))
            m = 0
            while m < 9:
                if temp < d[m, 0]:
                    d[m + 1:9, :] = d[m:8, :]
                    d[m, 0] = temp
                    d[m, 1:11] = delta
                    d[m, 11] = i + 1
                    break

                m = m + 1

        for s in range(0, 3):
            e = np.array(d)
            d[0, 1:11] = e[0, 1:11] - st2[s, 0:10]
            d[0, 0] = np.matmul(w, np.conj(np.transpose(np.power(d[0, 1:11], 2))))
            d[0, 11:12 + s] = e[0, 11:12 + s]
            d[0, 12:13 + s] = 1
            for m in range(1, 8):
                delta = e[m, 1:11] - st2[0, 0:10]
                temp = np.matmul(w, np.conj(np.transpose(np.power(delta, 2))))
                for num in range(0, m):
                    if temp < d[num, 0]:
                        d[num + 1:9, :] = d[num:8, :]
                        d[num, 0] = temp
                        d[num, 1:11] = delta
                        d[num, 11:12 + s] = e[0, 11:12 + s]
                        d[num, 12 + s] = 1
                        break
                if temp >= d[m - 1, 0]:
                    d[m, 1:11] = delta
                    d[m, 0] = temp
                    d[m, 11:12 + s] = e[0, 11:12 + s]
                    d[0, 12:13 + s] = 1
            for j in range(0, 8):
                for k in range(0, 64):
                    delta = e[j, 1:11] - st2[s, k * 10: (k + 1) * 10]
                    temp = np.matmul(w, np.conj(np.transpose(np.power(delta, 2))))
                    for n in range(0, 8):
                        if temp < d[n, 0]:
                            d[n + 1:9, :] = d[n:8, :]
                            d[n, 0] = temp
                            d[n, 1:11] = delta
                            d[n, 11:12 + s] = e[j, 11:12 + s]
                            d[n, 12 + s] = k + 1
                            break
        g = d[0, 11:15]
        return g
    except Exception as e:
        raise e
