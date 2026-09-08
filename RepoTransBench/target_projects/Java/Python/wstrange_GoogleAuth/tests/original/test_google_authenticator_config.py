def test_default_constructor_and_getters():
    class DummyConfig:
        def getWindowSize(self):
            return 1
        def getCodeDigits(self):
            return 6
        def getKeyRepresentation(self):
            return "BASE32"
        def getTimeStepSizeInMillis(self):
            return 30000
        def getHmacHashFunction(self):
            return "HmacSHA1"
        def getNumberOfScratchCodes(self):
            return 5
        def getSecretBits(self):
            return 160

    config = DummyConfig()
    assert config.getWindowSize() >= 0
    assert config.getCodeDigits() >= 0
    assert config.getKeyRepresentation() is not None
    assert config.getTimeStepSizeInMillis() > 0
    assert config.getHmacHashFunction() is not None
    assert config.getNumberOfScratchCodes() >= 0
    assert config.getSecretBits() >= 0

def test_builder():
    class GoogleAuthenticatorConfigBuilder:
        def __init__(self):
            self.window_size = 4
            self.code_digits = 7
            self.key_representation = "BASE64"
            self.time_step_size_in_millis = 654321
            self.hmac_hash_function = "HmacSHA1"
            self.number_of_scratch_codes = 7
            self.secret_bits = 160
        def setWindowSize(self, x): self.window_size = x; return self
        def setCodeDigits(self, x): self.code_digits = x; return self
        def setKeyRepresentation(self, x): self.key_representation = x; return self
        def setTimeStepSizeInMillis(self, x): self.time_step_size_in_millis = x; return self
        def setHmacHashFunction(self, x): self.hmac_hash_function = x; return self
        def setNumberOfScratchCodes(self, x): self.number_of_scratch_codes = x; return self
        def setSecretBits(self, x): self.secret_bits = x; return self
        def build(self):
            class ResultConfig:
                def getWindowSize(inner): return self.window_size
                def getCodeDigits(inner): return self.code_digits
                def getKeyRepresentation(inner): return self.key_representation
                def getTimeStepSizeInMillis(inner): return self.time_step_size_in_millis
                def getHmacHashFunction(inner): return self.hmac_hash_function
                def getNumberOfScratchCodes(inner): return self.number_of_scratch_codes
                def getSecretBits(inner): return self.secret_bits
            return ResultConfig()

    builder = GoogleAuthenticatorConfigBuilder()
    config = builder.build()

    assert config.getWindowSize() == 4
    assert config.getCodeDigits() == 7
    assert config.getKeyRepresentation() == "BASE64"
    assert config.getTimeStepSizeInMillis() == 654321
    assert config.getHmacHashFunction() == "HmacSHA1"
    assert config.getNumberOfScratchCodes() == 7
    assert config.getSecretBits() == 160