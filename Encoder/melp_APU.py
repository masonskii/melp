def melp_APU(p3, rp3, G2, buffer):
    """
    Медианный фильтр
    :param p: окончательное значение ОТ
    :param rp3: соответствующая корреляция p3
    :param G2: усиление для второго подкадра
    :param buffer: буфер значений ОТ
    :return:
    pavg - среднее значение ОТ
    buffer - обновленный буфер
    """
    try:
        from statistics import median

        if rp3 > 0.8 and G2 > 30:
            buffer[0:2] = buffer[1:3]
            buffer[2] = p3
        else:
            buffer = [b * 0.95 + 2.5 for b in buffer]

        pavg = median(buffer)
        return pavg, buffer
    except Exception as e:
        raise e
