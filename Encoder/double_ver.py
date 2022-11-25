def double_ver(sig_in, pp, cor_p):
    """
    Удаление низкого ОТ
    :param sig_in: Входной сигнал
    :param pp: значение К
    :param cor_p: корреляция
    :return: cor_p
    """
    try:
        from Encoder.fpr import fpr

        np, ncor_p = fpr(sig_in, round(2 * pp))  # вычисление корреляции для удвоенного значения К
        if ncor_p < cor_p:  # если рассчитанное значение корреляции меньше входной,
            cor_p = ncor_p  # то оно присваивается входной
        return cor_p

    except Exception as e:
        raise e
