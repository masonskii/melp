import numpy as np
from dataclasses import dataclass

from matplotlib import pyplot as plt
from numpy import ndarray
from scipy import signal
from Encoder.coeff import dcr_num, dcr_den, butt_1000num, butt_1000den
from Encoder.pitch3 import *
from Encoder.d_lsf import d_lsf
from Encoder.find_harm import find_harm
from Encoder.intpitch import intpitch
from Encoder.lpc_residual import lpc_residual
from Encoder.lsf_clmp import lsf_clmp
from Encoder.melp_5b import melp_5b
from Encoder.melp_APU import melp_APU
from Encoder.melp_FMCQ import melp_FMCQ
from Encoder.melp_Qgain import melp_Qgain
from Encoder.melp_Qpitch import melp_Qpitch
from Encoder.melp_bpva import melp_bpva
from Encoder.melp_gain import melp_gain
from Encoder.melp_lpc import melp_lpc
from Encoder.melp_lpc2lsf import melp_lpc2lsf
from Encoder.melp_lsf21pc import melp_lsf21pc
from Encoder.melp_msvq import melp_msvq
from Encoder.pitch2 import pitch2


@dataclass
class Block:
    range: tuple[int, int]
    noise: ndarray
    lpc: ndarray
    signal: ndarray
    MSVQ: ndarray


dcr_num = np.array([0.9269, -3.7056, 5.5574, -3.7056, 0.9269])
dcr_den = np.array([1.00000000, -3.84610723, 5.55209760, -3.56516069, 0.85918839])
FRL = 180
cheb_s = np.zeros(4)


def open_file_signal(filename='output_sound.wav', FRL=180, fdtype='int32', adtype=float):
    """
    :param filename:   file with signal
    :param adtype:  Тип данных для массива
    :param fdtype: Тип данных для файла
    :param FRL: Длинна кадра
    :return:
        s - массив сигнала
        NFrame - Число кадров
    """
    try:
        if adtype == float:
            adtype = np.float64
        s = np.transpose(np.fromfile('output_sound.wav', dtype="uint8"))
        s = np.array(s[7 * 8 + 2:], dtype=float)
        s -= 128
        s /= 128
        s *= 32767

        Nframe = np.fix(len(s) / FRL)
        return s, int(Nframe)
    except Exception as e:
        raise e


C = []
s, nframe = open_file_signal()
sig_in = np.zeros(FRL * 2)
for i in range(nframe - 1):
    sig_in[:FRL] = sig_in[FRL:FRL * 2]
    sig_origin = s[i * FRL: (i + 1) * FRL]
    sig_in[FRL:FRL * 2], cheb_s = signal.lfilter(dcr_num, dcr_den, sig_origin, zi=cheb_s)

    koef_lpc = melp_lpc(sig_in[80:280])
    e_reside = lpc_residual(koef_lpc, sig_in)
    LSF = melp_lpc2lsf(koef_lpc)
    LSF = lsf_clmp(LSF)
    MSVQ = melp_msvq(koef_lpc, LSF)
    C.append(
        Block(range=(i * FRL, (i + 1) * FRL), noise=signal.lfilter(1, [1] + koef_lpc.tolist(), np.random.randn(400)),
              lpc=koef_lpc,
              signal=sig_in[80:280],
              MSVQ=MSVQ)
    )

"""for i in range(len(C)):
    plt.plot(np.convolve(C[i].signal / np.std(C[i].signal), np.ones(3)))
    plt.plot(np.convolve(C[i].noise[180:], np.ones(4)))
    plt.show()
"""
d_msvq = []
lpcs = []
for i in range(len(C)-1):
    d_msvq.append(d_lsf(C[i].MSVQ))
t0 = 1
for i in range(len(C)):
    T = 50
    factor = t0 / 180
    if i == 0:
        ls2 = d_msvq[i]
    else:
        ls2 = factor * (ls2 - ls1) + ls1
    lpcs.append(melp_lsf21pc(d_msvq[i]))
    ls1 = ls2
    t0 = t0 + T
for i in range(len(lpcs)):
    plt.plot(np.convolve(C[i].signal / np.std(C[i].signal), np.ones(3)))
    plt.plot(np.convolve(signal.lfilter(1, [1] + lpcs[i].tolist(), np.random.randn(400))), np.ones(3))
    plt.show()
    breakpoint()
