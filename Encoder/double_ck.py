import numpy as np
from Encoder.double_ver import double_ver
from Encoder.fpr import fpr


def double_ck(sig_in, p, Dth):
    """
    Определение ОТ с удвоенной точностью
    :param sig_in:  входной сигнал
    :param p: дробное значение ОТ
    :param Dth: пороговое значение
    :return:
    pc - значение ОТ (с двойной точностью)
    cor_pc - соответствующая корреляция
    """
    pmin = 20  # Минимальное значение ОТ
    pc, cor_pc = fpr(sig_in, np.around(p))  # улучшение дробного значения ОТ

    for i in np.arange(7):  # поиск лучшего ОТ
        k = 8 - i  # значение делителя
        temp_pit = np.around(pc / k)

        if temp_pit >= pmin:
            temp_pit, temp_cor = fpr(sig_in, temp_pit)  # улучшение дробного значение ОТ
            if temp_pit < 30:
                temp_cor = double_ver(sig_in, temp_pit, temp_cor)  # удаление низкого ОТ
            if temp_cor > Dth * cor_pc:
                pc, cor_pc = fpr(sig_in, round(temp_pit))  # улучшение дробного значения ОТ
                break
    if pc < 30:
        cor_pc = double_ver(sig_in, pc, cor_pc)  # удаление низкого ОТ

    return pc, cor_pc
