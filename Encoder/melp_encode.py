import struct

import numpy as np
import audioread
from numpy import ndarray
from scipy.signal import lfilter
import scipy
import matplotlib
from matplotlib import pyplot as plt
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
import scipy.io.wavfile as wav

__all__ = ['C', 'open_file_signal', 'encoder']


class C:
    def __init__(self, ls, qfm, g, pitch, vp, jt):
        self.ls = ls
        self.QFM = qfm
        self.G = g
        self.pitch = pitch
        self.vp = vp
        self.jt = jt


def open_file_signal(filename='output_sound.wav', FRL=180, fdtype='int32', adtype=float) -> tuple[ndarray, int]:
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


def encoder() -> tuple[list[C], ndarray]:
    """
    Инициализация
    """
    FRL = 180  # Длина кадра
    sig_in = np.zeros(FRL * 2)  # входной сигнал
    sig_1000 = np.zeros(FRL * 2)  # сигнал на входе ФНЧ (1000 Гц)
    melp_bands = np.zeros((5, (FRL * 2)))  # полосовые сигналы

    # начальные состояния
    cheb_s = np.zeros(4)
    butter_s = np.zeros(6)
    state_b = np.zeros((5, 6))
    state_e = np.zeros((4, 2))
    state_t = np.zeros((4, 6))
    state_syn = np.zeros(10)
    melp_envelopes = np.zeros((4, (FRL * 2)))  # огибающие полосовых сигналов
    pre_intp = 40
    frame_num = 320
    buffer = [50, 50, 50]  # буфер медианного фильтра ОТ
    pavg = 50  # значение ОТ для случая низкой корреляции значений ОТ,
    # определенных по речевому сигналу и сигналу остатка
    G2p = 20  # значение усиления для предыдущего кадра
    s, Nframe = open_file_signal()
    global Qpitch
    RESULT = []
    """
    """
    for i in np.arange(Nframe - 1):  # покадровый анализ речевого сигнала
        """
        Выборка куска сигнала
        """
        vp = np.zeros(5)
        sig_in[:FRL] = sig_in[FRL:FRL * 2]  # Обновление буфера фильтра Чебышева 4-го порядка
        sig_1000[:FRL] = sig_1000[FRL: FRL * 2]  # Обновление буфера ФНЧ с частотой среза 1000 Гц(ОТ)
        melp_bands[:, :FRL] = melp_bands[:, FRL: FRL * 2]  # Обновление буфера полосовых фильтров
        melp_envelopes[:, :FRL] = melp_envelopes[:, FRL:FRL * 2]  # обновление огибающих речи в полосах
        """Взятие нового кадра речи"""
        sig_origin = s[i * FRL: (i + 1) * FRL]
        """
        """

        """
        Фильтрация выбранного куска 
        """
        """Ослабление постоянной составляющей"""
        sig_in[FRL:FRL * 2], cheb_s = lfilter(dcr_num, dcr_den, sig_origin, zi=cheb_s)
        """Вычисление целочисленного значения ОТ"""
        sig_1000[FRL: FRL * 2], butter_s = lfilter(butt_1000num, butt_1000den, sig_in[FRL: FRL * 2],
                                                   zi=butter_s)

        """
        """

        """
        Начало подсчета коэффициентов
        """

        cur_intp = intpitch(sig_1000, 160, 40)
        """ АНАЛИЗ СИГНАЛА ПО ПОЛОСАМ 2
        Получение полос и огибающих сигнала"""
        melp_bands[:, FRL:FRL * 2], state_b, melp_envelopes[:, FRL:FRL * 2], state_e = melp_5b(
            sig_in[FRL:FRL * 2],
            state_b, state_e)
        """Вычисление дробного значения ОТ """
        p2, vp[0] = pitch2(melp_bands[0, :], cur_intp)
        """Анализ вокализованности полос"""
        vp[1:5] = melp_bpva(melp_bands, melp_envelopes, p2)
        r2 = vp[0]
        """ Определение джиттера """
        if vp[0] < 0.5:
            jitter = 1
        else:
            jitter = 0
        """LPC анализ"""
        koef_lpc = melp_lpc(sig_in[80:280])
        koef_lpc = koef_lpc * np.power(0.994, np.arange(2, 12))
        """Определение остатка предсказания"""
        e_resid = lpc_residual(koef_lpc, sig_in)
        """Окончательное определение вокализованности полос"""
        peak = np.sqrt(np.matmul(e_resid[105:265], np.conj(np.transpose(e_resid[105:265]))) / 160) / (
                np.sum(np.abs(e_resid[105:265])) / 160)
        if peak > 1.34:
            vp[0] = 1
        if peak > 1.6:
            vp[1:3] = 1
        """ Окончательное определение ОТ"""
        temp_s = np.zeros(6)
        fltd_resid, temp_s = lfilter(butt_1000num, butt_1000den, e_resid, zi=temp_s)
        temp_s = np.reshape(temp_s, (-1, 1))
        fltd_resid = np.append([0, 0, 0, 0, 0], fltd_resid)
        fltd_resid = np.append(fltd_resid, [0, 0, 0, 0, 0])
        p3, r3 = pitch3(sig_in, fltd_resid, p2, pavg)
        """Вычисление усиления """
        G = melp_gain(sig_in, vp[0], p2)
        """Обновление среднего значения ОТ"""
        pavg, buffer = melp_APU(p3, r3, G[1], buffer)
        pavg = int(pavg)
        """Преобразование коэффициентов ЛП в ЛСЧ"""
        LSF = melp_lpc2lsf(koef_lpc)
        """Расширение минимального расстояния"""
        LSF = lsf_clmp(LSF)
        """Много уровневое векторное квантование """
        MSVQ = melp_msvq(koef_lpc, LSF)
        """Квантование усиления"""
        QG = melp_Qgain(G2p, G)
        G2p = G[1]  # обновление значения усиления для предыдущего кадра
        """Квантование ОТ"""
        if vp[0] > 0.6:
            Qpitch = melp_Qpitch(p3)
        """Определение амплитуд фурье-спектра"""
        lsfs = d_lsf(MSVQ)  # определение вектора квантованных ЛСЧ
        lpc2 = melp_lsf21pc(lsfs)  # преобразование ЛСЧ в коэффициенты ЛП
        tresid2 = lpc_residual(lpc2, sig_in[75:285])  # Определение остатка предсказания по квантованным КЛП
        resid2 = np.zeros(512)  # дополнение нулями
        resid2[:200] = tresid2 * np.hamming(200)  # применение окна Хэмминга
        magf = np.abs(np.fft.fft(resid2))  # амплитуды фурье-спектра
        fm, Wf = find_harm(magf, p3)  # определение гармоник основной частоты
        """Квантование амплитуд фурье-спектра """
        QFM = melp_FMCQ(fm, Wf)
        """Формирование кадра передачи"""
        if vp[0] > 0.6:
            RESULT += [C(MSVQ, QFM, QG, Qpitch, np.around(vp[1:5]), jitter)]
        else:
            RESULT += [C(MSVQ, QFM, QG, 0, 0, 0)]
    return RESULT, s
