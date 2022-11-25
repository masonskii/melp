import numpy as np
from scipy.signal import lfilter, lfilter_zi


def d_lps(lpc_coeff, ae, state_syn):
    """
    Синтезирующий LPC фильтр
    :param lpc_coeff: интерполированные коэффициенты
    :param ae: сигнал с выхода блока адаптивной спектральной коррекции
    :param state_syn: начальное состояние фильтра синтеза
    :return:
    f - синтезированный PC
    state_syn - конечное состояние фильтра синтеза
    """
    coeff = np.append(1, lpc_coeff)
    f, state_syn = lfilter(1, coeff, ae, zi=state_syn)
    return f, state_syn
