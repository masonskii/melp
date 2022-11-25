from Decoder.d_pdfs import *

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
