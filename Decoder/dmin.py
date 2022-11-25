import numpy as np
from numpy import ndarray


def switch(array, T):
    temp = array[T - 10:T]
    array = array[:T - 10]
    array = np.append(temp, array)
    return array


def upload_date(*args) -> [int, ndarray]:
    T = np.fromfile(args[0], dtype='float')
    en = np.fromfile(args[1], dtype='float')
    return int(T), en


def get_T(T, jt):
    try:
        T = T * (1 + jt * 0.5 * (np.random.random() - 0.5))
        T = np.int32(np.around(T))
        if T > 160:
            T = 160
        elif T < 20:
            T = 20
        return T
    except Exception as e:
        raise e


def d_min(fm, T, jt, vp, state_pul, state_noi):
    try:
        from Decoder.coeff import melp_firs
        T = get_T(T, jt)
        m = np.zeros(int(T))
        m[0:10] = fm
        m[T - 10:T] = np.flip(fm)
        if T > 21:
            m[10:T - 10] = 1
        m = np.append(0, m)
        ep = np.conj(np.transpose(np.real(np.fft.ifft(m))))
        ep = switch(ep, T)
        ep = ep * np.sqrt(T) * 1000
        en = (np.random.sample(T) - 0.5) * 3464
        efirs = np.zeros((31, 1))
        pfirs = np.zeros((31, 1))
        melp_firs = np.array(melp_firs)
        for i in np.arange(0, 5):
            if vp[i] > 0.5:
                for j in np.arange(0, len(pfirs)):
                    pfirs[j, 0] = pfirs[j, 0] + melp_firs[j, i]
            else:
                for j in np.arange(0, len(efirs)):
                    efirs[j, 0] = efirs[j, 0] + melp_firs[j, i]
        efirs = np.reshape(efirs, (-1, 1))
        pfirs = np.reshape(pfirs, (-1, 1))
        ep = np.append(state_pul, ep)
        en = np.append(state_noi, en)
        e = np.zeros(T)
        for i in np.arange(T):
            temp1 = np.matmul(ep[i:30 + (i + 1)], pfirs)
            temp2 = np.matmul(en[i:30 + (i + 1)], efirs)
            e[i] = np.sum(temp1 + temp2)
        if T < 30:
            state_pul = np.append(np.zeros(30 - T), ep[0:T])
            state_noi = np.append(np.zeros(30 - T), en[0:T])
        else:
            state_pul = ep[T - 30:T]
            state_noi = en[T - 30:T]
        return np.conj(np.transpose(e)), state_pul, state_noi, T
    except Exception as e:
        raise e
