import os
import numpy as np
import tempfile
import pickle

import pytest

# Mock size for LWE n
n = 10

class SecretKey(np.ndarray):
    def __new__(cls):
        return np.zeros(n, dtype=int).view(cls)

class CipherText:
    def __init__(self):
        self.a = np.zeros(n, dtype=int)
        self.b = 0

def SaveSecretKey(sk, fname):
    with open(fname, "wb") as f:
        pickle.dump(sk, f)

def LoadSecretKey(fname):
    with open(fname, "rb") as f:
        return pickle.load(f)

def SaveCipherText(ct, fname):
    with open(fname, "wb") as f:
        pickle.dump({'a': ct.a, 'b': ct.b}, f)

def LoadCipherText(fname):
    with open(fname, "rb") as f:
        data = pickle.load(f)
        ct = CipherText()
        ct.a = data['a']
        ct.b = data['b']
        return ct

def test_secret_key_save_load():
    sk = SecretKey()
    for i in range(n):
        sk[i] = i % 2
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        fname = tf.name
    try:
        SaveSecretKey(sk, fname)
        loaded = LoadSecretKey(fname)
        assert loaded[0] == sk[0]
        assert loaded[n-1] == sk[n-1]
    finally:
        os.remove(fname)

def test_cipher_text_save_load():
    ct = CipherText()
    for i in range(n):
        ct.a[i] = i
    ct.b = 12345
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        fname = tf.name
    try:
        SaveCipherText(ct, fname)
        loaded = LoadCipherText(fname)
        assert loaded.b == 12345
    finally:
        os.remove(fname)