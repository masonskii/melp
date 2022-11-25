def melp_bpva(melp_bands, melp_envelopes, p2):
    """
    Вариант определения вокализованности полос
    :param melp_bands: полосовые сигналы
    :param melp_envelopes: огибающие полосовых сигналов
    :param p2: дробное значение ОТ
    :return:
    vbp - вокализованность полос
    """
    try:
        import numpy as np
        from Encoder.fpr import fpr

        p2 = np.around(p2)  # окгруление до целого
        p = np.zeros(2)
        r = np.zeros(2)
        vbp = np.zeros(4)
        for i in np.arange(4):
            k = i + 1
            p[0], r[0] = fpr(melp_bands[k, :], p2)  # определение корреляции между полосовым сигналом и значением ОТ
            p[1], r[1] = fpr(melp_envelopes[i, :], p2)  # определение корреляции между огибающей и значением ОТ

            r[1] = r[1] - 0.1
            # определение большего коэффициента корреляции
            if r[1] > r[0]:
                temp = r[1]
            else:
                temp = r[0]
            # принятие решения о вокализованности полос
            if temp > 0.6:
                vbp[i] = 1
            else:
                vbp[i] = 0

        # если первые три полосы невокализованные, то четвертая тоже невокализованная
        if vbp[0] == 0 and vbp[1] == 0 and vbp[2] == 0:
            vbp[3] = 0
        return vbp
    except Exception as e:
        raise e
