import scipy.signal
import sounddevice as sd
import numpy as np
from scipy.fft import rfft, rfftfreq
from matplotlib import pyplot as plt
from numpy import ndarray
from Decoder.melp_decode import decode
from Encoder.melp_encode import encoder


def sound_wav(audio, is_play=False):
    if is_play:
        sd.play(np.array((audio[250:]), dtype=np.float64)*2500000, 8000)
        sd.wait()
    else:
        return


def show_plot(*args):
    for i in args:
        plt.plot(i[250:])
    plt.xlabel('Время')
    plt.title('График сравнения сигналов до и после обработки')

    plt.show()


def show_struct(struct):
    print("LS,\tQFM,\tG,\tPITCH,\tVP,\tJT")
    for i in struct:
        print(f"{i.ls},\t{i.QFM},\t{i.G},\t{i.pitch},\t{i.vp},\t{i.jt}\r")


if __name__ == '__main__':
    print('Start codec')
    params, signal = encoder()
    print('show result')
    show_struct(params)
    print('end codec')
    print('Start decodec')
    S, v = decode(params)
    show_plot(S)
    print('Result:')
    show_plot(S)
    sound_wav(S, True)  # TODO: Все еще шумит как не в себя
