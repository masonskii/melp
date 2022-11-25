def melp_gain(s, vbp1, p2):
    """
    Оценивание усиления
    :param s: входной сигнал
    :param vbp: вокализированность первой полосы
    :param p2: дробное значение К
    :return:
    G - array, where ->
        G1 - усиление для первого подкадра
        G2 - усиление для второго подкадра

    """
    try:
        import numpy as np

        k = 1
        Ltmp = p2
        Lfr = p2

        if vbp1 > 0.6:
            while Ltmp < 180:  # определение целого числа периодов к
                k = k + 1
                Lfr = Ltmp
                Ltmp = p2 * k
        else:
            Lfr = 120  # длительность сигнала, включающего целое число периодов
        HL = np.int32(np.around(Lfr / 2))
        Lfr = np.int32(HL * 2)
        G = np.zeros(2)
        # Усиление для первого подкадра
        G[0] = 10 * np.log10(0.01 + np.matmul(s[90 - HL:90 + HL], np.conj(np.transpose(s[90 - HL:90 + HL]) / Lfr)))
        G[1] = 10 * np.log10(0.01 + np.matmul(s[180 - HL:180 + HL], np.conj(np.transpose(s[180 - HL:180 + HL]) / Lfr)))

        for i in np.arange(1):
            if G[i] < 0:
                G[i] = 0
        return G
    except Exception as e:
        raise e
