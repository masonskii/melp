def d_gains(G, G2pt, G2p_error):
    """
    Восстановление усилений
    :param G:принятое значение усиления
    :param G2pt:значение усиления для предыдущего кадра
    :param G2p_error:величина, указывающая на различие (>5 Дб) между значениями
              усиления для второго подкадра текущего и предыдущего кадров
    :return:
     G1        - значение усиления для первого подкадра
     G2        - значение усиления для второго подкадра
     G2pt      - значение усиления для предыдущего кадра
     G2p_error - величина, указывающая на различие (>5 Дб) между значениями
               усиления для второго подкадра текущего и предыдущего кадров

    """

    global gain_max, gain_min
    delta = 67 / 32
    G2 = (G[1] + 0.5) * delta + 10
    if G[0] == 0:
        if abs(G2 - G2pt) > 5:
            if G2p_error == 0:
                G2 = G2pt

            G2p_error = 1
        else:
            G2p_error = 0
        G1 = 0.5 * (G2 + G2pt)
    else:
        gain_max = max(G2pt, G2) + 6
        gain_min = min(G2pt, G2) - 6
        if gain_min < 10:
            gain_min = 10
        if gain_max > 77:
            gain_max = 77
        G1 = (G[0] - 1) * (gain_max - gain_min) / 6 + gain_min
        G2p_error = 0
    G2pt = G2
    return G1, G2, G2pt, G2p_error

