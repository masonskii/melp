def melp_lpc(s):
    """
    LPС Анализ
    :param s: входной сигнал
    :return:  f - выходной сигнал
    """
    try:
        import numpy as np
        from Encoder.lpc import lpc

        a = np.zeros(10)
        v = s * np.conj(np.transpose(np.hamming(200)))
        a, _ = lpc(v, N=10)  # N = order
        return a
    except Exception as e:
        raise e
