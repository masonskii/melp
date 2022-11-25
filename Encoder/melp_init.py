import numpy as np

from scipy.io import wavfile

# инициализация переменных и констант
global FMCQ_CODEBOOK
global Wf
global stage1, stage2

# Источник речевого сигнала

# f = wavfile.read('output_sound.wav')
# f = open('output_sound.wav', 'rb')
s = np.transpose(np.fromfile('output_sound_my.wav', dtype="uint8"))
s = np.array(s[7 * 8 + 2:], dtype=np.float64)
s = s - 128
s = s / 128
s = s * 32767
FRL = 180  # Длина кадра
Nframe = int(np.fix(len(s) / FRL))  # Число кадров во входном сигнале
# Начальные условия

sig_in = np.zeros(FRL * 2)  # входной сигнал
sig_1000 = np.zeros(FRL * 2)  # сигнал на входе ФНЧ (1000 Гц)
melp_bands = np.zeros((5, (FRL * 2)))  # полосовые сигналы

# начальные состояния 
cheb_s = np.zeros(4)
butter_s = np.zeros(6)
state_b = np.zeros((5, 6))
state_e = np.zeros((4, 2))
state_t = np.zeros((4, 6))
state_syn = np.zeros(10)  # !!!!!!!!!!!!!!
melp_envelopes = np.zeros((4, (FRL * 2)))  # огибающие полосовых сигналов
pre_intp = 40
frame_num = 320
buffer = [50, 50, 50]  # буфер медианного фильтра ОТ
pavg = 50  # значение ОТ для случая низкой корреляции значений ОТ,
# определенных по речевому сигналу и сигналу остатка
G2p = 20  # значение усиления для предыдущего кадра
