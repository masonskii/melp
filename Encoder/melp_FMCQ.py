def melp_FMCQ(mag, Wf):
    """
    Векторный кватователь амплитуд Фурье - спектра
    :param mag: амплитуды Фурье - спектра
    :param Wf:  веса для Евклидова расстояния гармоник Фурье
    :return: 
    f - индекс в КК амплиуд Фурье - спектра
    """
    try:
        import numpy as np

        from Encoder.codebook_fmcq import FMCQ_CODEBOOK

        fmcq = np.asarray(FMCQ_CODEBOOK, dtype=np.float64)
        f = 0
        temp = 1000
        for i in np.arange(256):
            u = fmcq[i, :10] - mag
            rms = np.matmul(Wf, np.conj(np.transpose(u * u)))
            if rms < temp:
                temp = rms
                f = i+1

        return f
    except Exception as e:
        raise e
