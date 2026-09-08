def test_constructor_and_getters():
    class DummyConfig: pass
    key = "SECRETKEY"
    verification_code = 123456
    scratch_codes = [111, 222]
    class GoogleAuthenticatorKey:
        def __init__(self, config, key, verification_code, scratch_codes):
            self._key = key
            self._verification_code = verification_code
            self._scratch_codes = scratch_codes
        def getKey(self): return self._key
        def getVerificationCode(self): return self._verification_code
        def getScratchCodes(self): return self._scratch_codes
    gak = GoogleAuthenticatorKey(DummyConfig(), key, verification_code, scratch_codes)
    assert gak.getKey() == key
    assert gak.getVerificationCode() == verification_code
    assert gak.getScratchCodes() == scratch_codes

def test_empty_scratch_codes():
    class DummyConfig: pass
    key = "FOO"
    verification_code = 0
    scratch_codes = []
    class GoogleAuthenticatorKey:
        def __init__(self, config, key, verification_code, scratch_codes):
            self._key = key
            self._verification_code = verification_code
            self._scratch_codes = scratch_codes
        def getKey(self): return self._key
        def getVerificationCode(self): return self._verification_code
        def getScratchCodes(self): return self._scratch_codes
    gak = GoogleAuthenticatorKey(DummyConfig(), key, verification_code, scratch_codes)
    assert gak.getKey() == key
    assert gak.getVerificationCode() == verification_code
    assert gak.getScratchCodes() == scratch_codes