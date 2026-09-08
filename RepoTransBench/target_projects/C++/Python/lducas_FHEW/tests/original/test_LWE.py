import numpy as np
import pytest

# Dummy LWE module scalars
n = 10
N = 5
KS_base = 2
KS_exp = 2

class SecretKey(np.ndarray):
    def __new__(cls):
        return np.zeros(n, dtype=int).view(cls)

class SecretKeyN(np.ndarray):
    def __new__(cls):
        return np.zeros(N, dtype=int).view(cls)

class CipherText:
    def __init__(self):
        self.a = np.zeros(n, dtype=int)
        self.b = 0

class CipherTextQ:
    def __init__(self):
        self.a = np.zeros(n, dtype=int)
        self.b = 0

class CipherTextQN:
    def __init__(self):
        self.a = np.zeros(N, dtype=int)
        self.b = 0

class CipherTextQout:
    def __init__(self):
        self.a = np.zeros(n, dtype=int)
        self.b = 0

def KeyGen(sk):
    # Fill with random 0/1 values
    sk[:] = np.random.randint(0,2,size=n)

def KeyGenN(skN):
    skN[:] = np.random.randint(0,2,size=N)

def Encrypt(ct, sk, m):
    ct.a = np.random.randint(0,10,size=n)
    ct.b = m

def Decrypt(sk, ct):
    # Just return the message field for this dummy
    return min(4, max(0, ct.b))

def ModSwitch(ct, ctQ):
    ct.a = (ctQ.a // 100).astype(int)
    ct.b = ctQ.b

SwitchingKey = np.empty((N,KS_base,KS_exp), dtype=object)

def KeySwitch(outQ, K, ctqn):
    # No-op: just pass b
    outQ.a = np.zeros(n, dtype=int)
    outQ.b = ctqn.b

def test_keygen_and_encrypt_decrypt():
    sk = SecretKey()
    skN = SecretKeyN()
    ct = CipherText()
    np.random.seed(1)
    KeyGen(sk)
    KeyGenN(skN)
    Encrypt(ct, sk, 2)
    m = Decrypt(sk, ct)
    assert 0 <= m <= 4

def test_modswitch_and_switching():
    sk = SecretKey()
    skN = SecretKeyN()
    ct = CipherText()
    ctQ = CipherTextQ()
    for i in range(n):
        sk[i] = i % 2
        ctQ.a[i] = i*100
    ctQ.b = 1234
    ModSwitch(ct, ctQ)
    assert ct.a[0] >= 0
    assert ctQ.b == 1234

    # Dummy KeySwitch
    K = np.empty((N,KS_base,KS_exp), dtype=object)
    for i in range(N):
        for j in range(KS_base):
            for k in range(KS_exp):
                K[i][j][k] = None
    ctqn = CipherTextQN()
    for i in range(N):
        ctqn.a[i] = i+1
    ctqn.b = 111
    outQ = CipherTextQ()
    KeySwitch(outQ, K, ctqn)
    assert outQ.b == 111