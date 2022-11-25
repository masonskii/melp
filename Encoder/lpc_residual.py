def lpc_residual(lpcs, sig_in):
    """
    Определение остатка предсказания
    :param lpcs: коэффициенты ЛП
    :param sig_in: входной сигнал
    :return:
    exc - сигнал остатка предсказания
    """
    try:
        import numpy as np
        from scipy.signal import lfilter

        exc = lfilter(np.append(1, lpcs), 1, sig_in)
        return exc[10:]
    except Exception as e:
        raise e
