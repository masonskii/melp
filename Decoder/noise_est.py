def noise_est(gain, G_n):
    """
    Оценка шума
    :param gain:значение усиления
    :param G_n:уровень шума
    :return: G_n  - уровень шума
    """
    try:
        from Decoder.d_init import Cup, Cdown

        if gain > G_n + Cup:
            G_n = G_n + Cup
        elif gain < G_n - Cdown:
            G_n = G_n - Cdown
        else:
            G_n = gain

        if G_n < 10:
            G_n = 10
        elif G_n > 20:
            G_n = 20

        return G_n
    except Exception as e:
        raise e
