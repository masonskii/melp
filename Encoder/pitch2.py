def pitch2(sig, intp):
    """
    Улучшение дробного значения ОТ в полосе 0-500 Гц
    :param sig: входой сигнал
    :param intp: целочисленное значение ОТ
    :return:
    p - дробное значение ОТ
    r - соответствующая корелляция
    """
    try:
        from Encoder.fpr import fpr
        from Encoder.intpitch import intpitch

        low = intp - 5  # определение нижней границы поиска задержки ОТ (не ниже 20)
        if low < 20:
            low = 20

        up = intp + 5  # определение верхней границы поиска задержки ОТ (не выше 160)
        if up > 160:
            up = 160

        p = intpitch(sig, up, low)  # определение значения ОТ в указанных пределах

        p, r = fpr(sig, p)  # улучшение дробного значения ОТ

        return p, r
    except Exception as e:
        raise e
