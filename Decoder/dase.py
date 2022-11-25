def d_ase(e, lpcs, G, Gn, u, T, state_ase, state_tilt):
    try:
        import numpy as np

        ppp = (G - Gn - 12) / 18
        if ppp < 0:
            ppp = 0
        if ppp > 1:
            ppp = 1

        a = 0.5 * np.power(ppp, np.arange(1, 11))
        b = 0.8 * ppp
        a = np.append(1, a)
        b = np.power(b, np.arange(1, 11))
        a = np.multiply(a, np.append(1, lpcs))
        b = np.multiply(b, lpcs)
        a = np.reshape(np.flip(a), (-1, 1))
        b = np.reshape(np.flip(b), (-1, 1))
        u = ppp * u
        buffer = state_ase
        f = np.zeros(T)
        for i in range(0, T):
            buffer = np.append(buffer, e[i] - np.matmul(buffer[i:i + 10], b))
            buffer[i] = np.matmul(buffer[i:i + 11], a)
            f[i] = buffer[i] + u * state_tilt
            state_tilt = buffer[i]

        state_ase = buffer[T:T + 10]
        return f, state_ase, state_tilt
    except Exception as e:
        raise e
