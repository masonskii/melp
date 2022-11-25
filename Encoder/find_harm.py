def find_harm(res, p3):
    """
    :param res: амплитудный спектр сигнал остатка по квантованным
    :param p3: окончательный ОТ
    :return:
        mag - амплитуды фурье-спектра
        Wf - веса для евклидова расстояния гармоник
    """
    try:
        import numpy as np

        down = int(np.fix(256 / p3))  # нижний уровень основной частоты
        M = int(np.fix(p3 / 4))  # число гармоник
        Wf = np.zeros(10)
        if M < 10:
            mag = np.zeros(M)
            for i in np.arange(M):
                up = np.int32(np.fix((i + 0.5 + 1) * 512 / p3))
                mag[i] = np.max(res[down:up])
                down = up
            mag = mag * np.sqrt(M) / np.linalg.norm(mag)
            temp = np.ones(10 - M)
            mag = np.append(mag, temp)
        else:
            mag = np.zeros(10)
            for i in np.arange(10):
                up = np.int32(np.fix((i + 0.5 + 1) * 512 / p3))
                mag[i] = np.max(res[down:up])
                down = up
            mag = mag * np.sqrt(10) / np.linalg.norm(mag)
        w0 = 2 * np.pi / p3
        for i in np.arange(10):
            Wf[i] = 117 / (25 + 75 * np.power(1 + 1.4 * np.sqrt(w0 * (i + 1) / (0.25 * np.pi)), 0.69))
        return mag, Wf
    except Exception as e:
        raise e
