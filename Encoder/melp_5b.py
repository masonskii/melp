def melp_5b(sig_in, state_b, state_e):
    """
    Расчет 5 полосовых сигналов и огибающих для 2 - 5 полос
    :param sig_in: входной сигнал
    :param state_b: исходные состояния полосовых фильтров
    :param state_e: исходные состояния фильтров огибающих
    :return:
    bands - полосовые сигналы
    state_b - конечные состояния полосовых фильтров
    envelopes - огибающие полосовых сигналов
    state_e - конечные состояния фильтров огибающих
    """
    try:
        import numpy as np
        from scipy.signal import lfilter

        from Encoder.coeff import butt_bp_num, butt_bp_den, smooth_num, smooth_den

        bands = np.zeros((5, 180))
        envelopes = np.zeros((4, 180))
        b = np.asarray(butt_bp_num).reshape(5, 7)
        a = np.asarray(butt_bp_den).reshape(5, 7)
        for i in np.arange(5):  # фильтрация в каждой из 5 полос
            bands[i, :], state_b[i, :] = lfilter(b[i, :], a[i, :], sig_in, zi=state_b[i, :])
        temp1 = np.abs(bands[0:4, :])  # абсолютные значения полосовых (1-4) сигналов
        a = np.asarray(smooth_den).reshape(1, 3)
        b = np.asarray(smooth_num).reshape(1, 3)
        for i in np.arange(4):
            envelopes[i, :], state_e[i, :] = lfilter(b[0, :], a[0, :], temp1[i, :],
                                                     zi=state_e[i, :])  # сглаживающий фильтр

        return bands, state_b, envelopes, state_e
    except Exception as e:
        raise e
