def noise_sup(gain, G_n):
    """
    Подавление шума
    :param gain: значение усиления
    :param G_n: уровень шума
    :return: G_n уровень шума
    """
    try:
        import numpy as np

        max_noise = 20
        max_atten = 6
        if G_n > max_noise:
            G_n = max_noise
        gain_lev = gain - G_n - 3
        if gain_lev > 0.001:
            suppress = -10 * np.log10(1 - 10 ** (-0.1 * gain_lev))
            if suppress > max_atten:
                suppress = max_atten
        else:
            suppress = max_atten
        gain = gain - suppress
        return gain
    except Exception as e:
        raise e
