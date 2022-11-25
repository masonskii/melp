def d_gains(G, G2pt, G2p_error):
    try:
        import numpy as np

        global gain_max, gain_min
        delta = 67 / 32
        G2 = (G[1] + 0.5) * delta + 10
        if G[1] == 0:
            if np.abs(G2 - G2pt) > 5:
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
        G1 = (G[1] - 1) * (gain_max - gain_min) / 6 + gain_min
        G2p_error = 0
        G2pt = G2
        return G1, G2, G2pt, G2p_error
    except Exception as e:
        raise e
