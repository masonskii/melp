def fpr(sig, T):
    """
    Улучшение дробного значения ОТ
    :param sig: входной сигнал
    :param T:входное целочисленное значение
    :return:
    fp  - дробное значение ќ“
    fr  - соответствующа¤ коррел¤ци¤
    """
    try:
        import cmath
        import numpy as np
        T = int(T)
        k = int(T / 2)
        # Автокорреляция
        c0_tm1 = int(np.matmul(sig[100 - k:259 - k],
                               np.conj(np.transpose(np.reshape(sig[100 - k + T - 1:259 - k + T - 1], (1, -1))))))
        c0_t1 = int(np.matmul(sig[100 - k:259 - k], np.conj(
            np.transpose(np.reshape(sig[100 - k + T + 1:259 - k + T + 1], (1, -1))))))
        c0_t = int(np.matmul(sig[100 - k:259 - k],
                             np.conj(np.transpose(np.reshape(sig[100 - k + T:259 - k + T], (1, -1))))))
        if c0_tm1 > c0_t1:  # Оценка диапазона fp
            c0_t1 = c0_t
            c0_t = c0_tm1
            T = T - 1

        ct_t = int(np.matmul(sig[100 - k + T:259 - k + T],
                             np.conj(np.transpose(np.reshape(sig[100 - k + T:259 - k + T], (1, -1))))))
        c0_0 = int(np.matmul(sig[100 - k:259 - k], np.conj(np.transpose(np.reshape(sig[100 - k:259 - k], (1, -1))))))

        ct_t1 = int(np.matmul(sig[100 - k + T:259 - k + T],
                              np.conj(np.transpose(np.reshape(sig[100 - k + T + 1:259 - k + T + 1], (1, -1))))))
        ct1_t1 = int(np.matmul(sig[100 - k + T + 1:259 - k + T + 1],
                               np.conj(np.transpose(np.reshape(sig[100 - k + T + 1:259 - k + T + 1], (1, -1))))))

        # Параметр корреляции
        den = c0_t1 * (ct_t - ct_t1) + c0_t * (ct1_t1 - ct_t1)  # Знаменатель delta
        if abs(den) > 0.01:
            delta = (c0_t1 * ct_t - c0_t * ct_t1) / den
        if abs(den) < 0.01:
            delta = 0.5

        # Проверка граничных условий для параметра корреляции

        if delta < -1:
            delta = -1
        if delta > 2:
            delta = 2

        fp = T + delta  # Добавление смещения к целочисленному значению к

        # Отчет соответствующей корреляции
        den = c0_0 * (ct_t * (1 - delta) ** 2 + 2 * delta * (1 - delta) * ct_t1 + delta ** 2 * ct1_t1)
        den = cmath.sqrt(den).real
        if den > 0.01:
            fr = ((1 - delta) * c0_t + delta * c0_t1) / den
        else:
            fr = 0

        # проверка граничных условий для задержки ќ
        if fp < 20:
            fp = 20
        if fp > 160:
            fp = 160

        return fp, fr

    except Exception as e:
        raise e
