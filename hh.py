import numpy as np
from dataclasses import dataclass

from matplotlib import pyplot as plt
from numpy import ndarray
from scipy import signal
from Encoder.lpc import lpc
from Encoder.LEVINSON import LEVINSON
from Encoder.melp_lpc import melp_lpc


@dataclass
class Block:
    range: tuple[int, int]
    noise: ndarray
    lpc: ndarray
    signal: ndarray


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
    C.append(Block(range=(i * FRL, (i + 1) * FRL), noise=signal.lfilter(1, [1] + koef_lpc.tolist(), np.random.randn(400)), lpc=koef_lpc,
                   signal=sig_in[80:280])
             )

for i in range(len(C)):
    plt.plot(np.convolve(C[i].signal / np.std(C[i].signal), np.ones(3)))
    plt.plot(np.convolve(C[i].noise[180:], np.ones(4)))
    plt.show()
    breakpoint()
