import numpy

__all__ = ["LEVINSON", "rlevinson"]


def LEVINSON(r, order=None, allow_singularity=False):
    T0 = numpy.real(r[0])
    T = r[1:]
    M = len(T)

    if order is None:
        M = len(T)
    else:
        assert order <= M, 'order must be less than size of the input data'
        M = order

    realdata = numpy.isrealobj(r)
    if realdata is True:
        A = numpy.zeros(M, dtype=float)
        ref = numpy.zeros(M, dtype=float)
    else:
        A = numpy.zeros(M, dtype=complex)
        ref = numpy.zeros(M, dtype=complex)

    P = T0

    for k in range(0, M):
        save = T[k]
        if k == 0:
            temp = -save / P
        else:
            # save += sum([A[j]*T[k-j-1] for j in range(0,k)])
            for j in range(0, k):
                save = save + A[j] * T[k - j - 1]
            temp = -save / P
        if realdata:
            P = P * (1. - temp ** 2.)
        else:
            P = P * (1. - (temp.real ** 2 + temp.imag ** 2))
        if P <= 0 and allow_singularity == False:
            raise ValueError("singular matrix")
        A[k] = temp
        ref[k] = temp  # save reflection coeff at each step
        if k == 0:
            continue

        khalf = (k + 1) // 2
        if realdata is True:
            for j in range(0, khalf):
                kj = k - j - 1
                save = A[j]
                A[j] = save + temp * A[kj]
                if j != kj:
                    A[kj] += temp * save
        else:
            for j in range(0, khalf):
                kj = k - j - 1
                save = A[j]
                A[j] = save + temp * A[kj].conjugate()
                if j != kj:
                    A[kj] = A[kj] + temp * save.conjugate()

    return A, P, ref


def rlevinson(a, efinal):
    """computes the autocorrelation coefficients, R based
    on the prediction polynomial A and the final prediction error Efinal,
    using the stepdown algorithm.

    Works for real or complex data

    :param a:
    :param efinal:

    :return:
        * R, the autocorrelation
        * U  prediction coefficient
        * kr reflection coefficients
        * e errors

    A should be a minimum phase polynomial and A(1) is assumed to be unity.

    :returns: (P+1) by (P+1) upper triangular matrix, U,
        that holds the i'th order prediction polynomials
        Ai, i=1:P, where P is the order of the input
        polynomial, A.



             [ 1  a1(1)*  a2(2)* ..... aP(P)  * ]
             [ 0  1       a2(1)* ..... aP(P-1)* ]
       U  =  [ .................................]
             [ 0  0       0      ..... 1        ]

    from which the i'th order prediction polynomial can be extracted
    using Ai=U(i+1:-1:1,i+1)'. The first row of U contains the
    conjugates of the reflection coefficients, and the K's may be
    extracted using, K=conj(U(1,2:end)).

    .. todo:: remove the conjugate when data is real data, clean up the code
       test and doc.

    """
    a = numpy.array(a)
    realdata = numpy.isrealobj(a)

    assert a[0] == 1, 'First coefficient of the prediction polynomial must be unity'

    p = len(a)

    if p < 2:
        raise ValueError('Polynomial should have at least two coefficients')

    if realdata == True:
        U = numpy.zeros((p, p))  # This matrix will have the prediction
        # polynomials of orders 1:p
    else:
        U = numpy.zeros((p, p), dtype=complex)
    U[:, p - 1] = numpy.conj(a[-1::-1])  # Prediction coefficients of order p

    p = p - 1
    e = numpy.zeros(p)

    # First we find the prediction coefficients of smaller orders and form the
    # Matrix U

    # Initialize the step down

    e[-1] = efinal  # Prediction error of order p

    # Step down
    for k in range(p - 1, 0, -1):
        [a, e[k - 1]] = levdown(a, e[k])
        U[:, k] = numpy.concatenate((numpy.conj(a[-1::-1].transpose()),
                                     [0] * (p - k)))

    e0 = e[0] / (1. - abs(a[1] ** 2))  # % Because a[1]=1 (true polynomial)
    U[0, 0] = 1  # % Prediction coefficient of zeroth order
    kr = numpy.conj(U[0, 1:])  # % The reflection coefficients
    kr = kr.transpose()  # % To make it into a column vector

    #   % Once we have the matrix U and the prediction error at various orders, we can
    #  % use this information to find the autocorrelation coefficients.

    R = numpy.zeros(1, dtype=complex)
    # % Initialize recursion
    k = 1
    R0 = e0  # To take care of the zero indexing problem
    R[0] = -numpy.conj(U[0, 1]) * R0  # R[1]=-a1[1]*R[0]

    # Actual recursion
    for k in range(1, p):
        r = -sum(numpy.conj(U[k - 1::-1, k]) * R[-1::-1]) - kr[k] * e[k - 1]
        R = numpy.insert(R, len(R), r)

    # Include R(0) and make it a column vector. Note the dot transpose

    # R = [R0 R].';
    R = numpy.insert(R, 0, e0)
    return R, U, kr, e


def levdown(anxt, enxt=None):
    """One step backward Levinson recursion

    :param anxt:
    :param enxt:
    :return:
        * acur the P'th order prediction polynomial based on the P+1'th order prediction polynomial, anxt.
        * ecur the the P'th order prediction error  based on the P+1'th order prediction error, enxt.

    ..  * knxt the P+1'th order reflection coefficient.

    """
    # % Some preliminaries first
    # if nargout>=2 & nargin<2
    #    raise ValueError('Insufficient number of input arguments');
    if anxt[0] != 1:
        raise ValueError('At least one of the reflection coefficients is equal to one.')
    anxt = anxt[1:]  # Drop the leading 1, it is not needed
    #  in the step down

    # Extract the k+1'th reflection coefficient
    knxt = anxt[-1]
    if knxt == 1.0:
        raise ValueError('At least one of the reflection coefficients is equal to one.')

    # A Matrix formulation from Stoica is used to avoid looping
    acur = (anxt[0:-1] - knxt * numpy.conj(anxt[-2::-1])) / (1. - abs(knxt) ** 2)
    ecur = None
    if enxt is not None:
        ecur = enxt / (1. - numpy.dot(knxt.conj().transpose(), knxt))

    acur = numpy.insert(acur, 0, 1)

    return acur, ecur


def levup(acur, knxt, ecur=None):
    """LEVUP  One step forward Levinson recursion

    :param acur:
    :param knxt:
    :return:
        * anxt the P+1'th order prediction polynomial based on the P'th order prediction polynomial, acur, and the
          P+1'th order reflection coefficient, Knxt.
        * enxt the P+1'th order prediction  prediction error, based on the P'th order prediction error, ecur.


    :References:  P. Stoica R. Moses, Introduction to Spectral Analysis  Prentice Hall, N.J., 1997, Chapter 3.
    """
    if acur[0] != 1:
        raise ValueError('At least one of the reflection coefficients is equal to one.')
    acur = acur[1:]  # Drop the leading 1, it is not needed

    # Matrix formulation from Stoica is used to avoid looping
    anxt = numpy.concatenate((acur, [0])) + knxt * numpy.concatenate((numpy.conj(acur[-1::-1]), [1]))

    enxt = None
    if ecur is not None:
        # matlab version enxt = (1-knxt'.*knxt)*ecur
        enxt = (1. - numpy.dot(numpy.conj(knxt), knxt)) * ecur

    anxt = numpy.insert(anxt, 0, 1)

    return anxt, enxt
