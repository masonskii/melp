def d_disp(sig_in, state_disp, disperse):
    try:
        import numpy as np

        buffer = np.append(state_disp, sig_in)
        f = np.zeros(180)
        for i in np.arange(0, 180):
            f[i] = np.matmul(buffer[i:i + 65], disperse)

        state_disp = sig_in[115:180]
        return f, state_disp
    except Exception as e:
        raise e
