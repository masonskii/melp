def intpitch(ss, ipmax, ipmin):
    """
    Определение целочисленного значения ОТ
    Предусловие: текущий и следующий кадр - ss[0:360]
    постусловие: автокорреляция
    :param ss: входной сигнал
    :param ipmax: максимальное значение задержки ОТ
    :param ipmin: минимальное зачение задержки ОТ
    :return: T - целочисленное значение задержки ОТ
    """
    try:
        import numpy as np

        r = 0  # максимальное значение нормированной функции автокорреляции
        T = 80  # начальное значение задержки ОТ
        r_new = 0  # текущее значение нормированной функции автокорреляции (НФАК)
        ipmax, ipmin = int(ipmax), int(ipmin)
        for tao in np.arange(ipmin, ipmax):
            k = np.int32(np.fix(tao / 2))
            c0_t = np.matmul(ss[100 - k:259 - k],
                                 np.transpose(np.reshape(ss[100 - k + tao: 259 - k + tao], (1, -1))))[
                0]  # числитель НФАК
            c0_0 = np.matmul(ss[100 - k:259 - k], np.transpose(np.reshape(ss[100 - k:259 - k], (1, -1))))[0]
            ct_t = np.matmul(ss[100 - k + tao:259 - k + tao],
                                 np.transpose(np.reshape(ss[100 - k + tao:259 - k + tao], (1, -1))))[0]
            den = c0_0 * ct_t  # знаменатель НФАК

            if den > 0:
                r_new = c0_t * c0_t / den  # расчет НФАК
            if r_new > r:
                r = r_new  # определение максимального значения НФАК
                T = tao  # и соответствующей задержки ОТ

        return T
    except Exception as e:
        raise e
