from scipy.signal import lfilter, lfilter_zi
from Decoder.d_pdfs import disperse
import numpy as np
from Decoder import dase, ddisp, dk1, dmin, dga
from Decoder.d_gains import d_gains
from Decoder.codebook_fmcq import FMCQ_CODEBOOK
from Decoder.d_lsf import d_lsf
from Decoder.melp_lsf21pc import melp_lsf21pc
from Decoder.noise_est import noise_est
from Decoder.noise_sup import noise_sup


def decode(C) -> tuple[list[float], list[float]]:
    Cup = 0.0337435
    Cdown = 0.135418

    t0 = 1
    p1 = 0

    ls1 = np.zeros(10)

    G2pt = 22
    G2p_error = 0
    Gno = 20
    G2p = 20
    u1 = 0
    jt1 = 0
    fm1 = np.ones(10)
    vp1 = []
    prev_scale = 1

    v = []
    state_pul = np.zeros(30)
    state_noi = np.zeros(30)
    state_syn = np.zeros(10)
    state_disp = np.zeros(64)
    state_tilt = 0
    state_ase = np.zeros(10)

    FRN = len(C)
    prev_sc = np.zeros((FRN, t0))
    vg = []
    vsig = []
    vh = []
    for i in np.arange(0, FRN-1):
        G1_1 = []
        G2_1 = []
        G1_2 = []
        G2_2 = []
        ls2 = np.array(d_lsf(C[i].ls))
        G1, G2, G2pt, G2p_error = d_gains(C[i].G, G2pt, G2p_error)
        G1_1.append(G1)
        G2_1.append(G2)
        Gno = noise_est(G1, Gno)
        G1 = noise_sup(G1, Gno)
        G1_2.append(G1)
        G2_2.append(G2)
        Gno = noise_est(G2, Gno)
        G2 = noise_sup(G2, Gno)
        if C[i].pitch != 0:
            fm2 = np.array(FMCQ_CODEBOOK[C[i].QFM, :])
            jt2 = C[i].jt
            vp2 = np.array([1, C[i].vp[0], C[i].vp[1], C[i].vp[2], C[i].vp[3]], dtype=float)
            p2 = C[i].pitch
        else:
            p2 = 0

        temp = melp_lsf21pc(ls2)
        u2 = max(0, dk1.d_k1(temp) * 0.5)

        if p1 == 0 and p2 != 0:
            fm1 = fm2
            p1 = p2
            jt1 = jt2
            vp1 = vp2
        else:
            vp1 = np.zeros(5)
        if t0 > 1:
            sig_fr = sig_fr[180:t0 + 179]
        else:
            sig_fr = []
        while t0 < 181:
            e = 0
            g = 0
            h = 0
            if p2 == 0:
                T = 50
                factor = t0 / 180
                if t0 < 91:
                    G = G2p + 2 * factor * (G1 - G2p)
                else:
                    G = G1 + (2 * factor - 1) * (G2 - G1)

                if i == 0:
                    lsfs = ls2
                else:
                    lsfs = factor * (ls2 - ls1) + ls1
                u = factor * (u2 - u1) + u1
            else:
                factor = t0 / 180
                jt = factor * (np.array(jt2) - np.array(jt1)) + np.array(jt1)
                fm = factor * (np.array(fm2) - np.array(fm1)) + np.array(fm1)
                vp = factor * (np.array(vp2) - np.array(vp1)) + np.array(vp1)
                if t0 < 91:
                    G = G2p + factor * (G1 - G2p) / 90
                else:
                    G = G1 + factor * (G2 - G1) / 90

                if G2 - G2p > 6:
                    factor = (G - G2p) / (G2 - G2p)

                if i == 0:
                    lsfs = ls2
                else:
                    lsfs = factor * (ls2 - ls1) + ls1
                T = factor * (p2 - p1) + p1
                u = factor * (u2 - u1) + u1

                if (G1 - G2p) > 6 and p1 > (2 * p2):
                    T = p2

            if p2 == 0:
                e = np.random.sample(T) - 1
            else:
                [e, state_pul, state_noi, T] = dmin.d_min(fm, T, jt, vp, state_pul, state_noi)
            lpcs = melp_lsf21pc(lsfs)
            [g, state_ase, state_tilt] = dase.d_ase(e, lpcs, G, Gno, u, T, state_ase, state_tilt)
            vg = np.concatenate([np.array(vg), np.array(g)])
            [h, state_syn] = lfilter(b=1, a=np.append(1, lpcs), x=g, zi=state_syn)
            vh = np.concatenate([np.array(vh), np.array(h)])
            [h, prev_scale] = dga.d_ga(h, G, prev_scale, T)
            sig_fr = np.concatenate([np.array(sig_fr), np.array(h)])
            t0 = t0 + T
        vsig = np.concatenate([np.array(vsig), np.array(sig_fr)])
        [temp, state_disp] = ddisp.d_disp(sig_fr, state_disp, disperse)
        v = np.concatenate([np.array(v), np.array(temp)])
        G2p = G2
        ls1 = ls2
        u1 = u2
        t0 = t0 - 180
        if p2 != 0:
            p1 = p2
            fm1 = fm2
            jt1 = jt2
    S = v / 32767 ** 2
    return S, v
