def pitch3(sig_in, resid, p2, pavg):
    """
    Окончательное определение ОТ
    ПРЕДУСЛОВИЯ: sin_in[0:360]; resid[0:360]
    :param sig_in:  сигнал с выхода префильтра
    :param resid: фильтрованный ФНЧ 1000 Гц сигнал остатка предсказаия
    :param p2: дробое значение ОТ
    :param pavg: среднее значение ОТ
    :return:
    p3 - дробное значение ОТ
    rp3 - соответствубщая корреляция
    """
    try:
        import numpy as np

        from Encoder.double_ck import double_ck
        from Encoder.fpr import fpr
        from Encoder.pitch2 import pitch2

        p2 = np.around(p2)  # округление дробного значения ОТ
        p3, rp3 = pitch2(resid, p2)  # вычисление дробного значения ОТ по сигналу остатка предсказания

        if rp3 >= 0.6:
            Dth = 0.5  # пороговое значение
            if p3 <= 100:
                Dth = 0.75  # пороговое значение

            p3, rp3 = double_ck(resid, p3, Dth)  # Определение ОТ с удвоенной точностью
        else:
            p3, rp3 = fpr(sig_in, p2)  # улучшение дробного значения
            if rp3 < 0.55:
                p3 = pavg
            else:
                Dth = 0.7
                if p3 <= 100:
                    Dth = 0.9

                p3, rp3 = double_ck(sig_in, p3, Dth)
        return p3, rp3
    except Exception as e:
        raise e
