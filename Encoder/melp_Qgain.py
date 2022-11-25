def melp_Qgain(G2p, G):
    """
    Квантование усиления
    :param G2p: усиление для предыдущего кадра
    :param G: усиление для текущего кадра
    :return:
        Q - квантованные усиления
    """
    try:
        import numpy as np
        Q = np.zeros(2)
        if G[0] <= 0:
            G[0] = 10
        if G[0] > 77:
            G[0] = 77

        if np.abs(G2p - G[1]) < 5 and (np.abs(G[0]) - 0.5 * (G[1] + G2p)) < 3:
            Q[0] = 0.0
        else:
            gain_max = max(G2p, G[1]) + 6
            gain_min = min(G2p, G[1]) - 6
            if gain_min < 10:
                gain_min = 10
            if gain_max > 77:
                gain_max = 77

            delta = (gain_max - gain_min) / 7
            temp = G[0] - gain_min
            Q[0] = 1 + np.fix(temp / delta)
            if Q[0] > 7:
                Q[0] = 7

        delta = 67 / 32
        Q[1] = np.fix((G[1] - 10) / delta)
        if Q[1] > 31:
            Q[1] = 31

        return Q
    except Exception as e:
        raise e
