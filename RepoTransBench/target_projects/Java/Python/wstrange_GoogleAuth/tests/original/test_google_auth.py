import pytest
import time
import base64
import binascii

# Dummy stubs for the classes, these must be replaced with real implementations.
class GoogleAuthenticatorConfig:
    def __init__(self, window_size=1, code_digits=6, key_representation="BASE32",
                 time_step_size_in_millis=30000, hmac_hash_function="HmacSHA1",
                 number_of_scratch_codes=5, secret_bits=160):
        self._window_size = window_size
        self._code_digits = code_digits
        self._key_representation = key_representation
        self._time_step_size_in_millis = time_step_size_in_millis
        self._hmac_hash_function = hmac_hash_function
        self._number_of_scratch_codes = number_of_scratch_codes
        self._secret_bits = secret_bits

    def getWindowSize(self):
        return self._window_size
    def getCodeDigits(self):
        return self._code_digits
    def getKeyRepresentation(self):
        return self._key_representation
    def getTimeStepSizeInMillis(self):
        return self._time_step_size_in_millis
    def getHmacHashFunction(self):
        return self._hmac_hash_function
    def getNumberOfScratchCodes(self):
        return self._number_of_scratch_codes
    def getSecretBits(self):
        return self._secret_bits

    class GoogleAuthenticatorConfigBuilder:
        def __init__(self):
            self.window_size = 1
            self.code_digits = 6
            self.key_representation = "BASE32"
            self.time_step_size_in_millis = 30000
            self.hmac_hash_function = "HmacSHA1"
            self.number_of_scratch_codes = 5
            self.secret_bits = 160

        def setWindowSize(self, win):
            self.window_size = win
            return self
        def setCodeDigits(self, x):
            self.code_digits = x
            return self
        def setKeyRepresentation(self, rep):
            self.key_representation = rep
            return self
        def setTimeStepSizeInMillis(self, t):
            self.time_step_size_in_millis = t
            return self
        def setHmacHashFunction(self, fn):
            self.hmac_hash_function = fn
            return self
        def setNumberOfScratchCodes(self, n):
            self.number_of_scratch_codes = n
            return self
        def setSecretBits(self, n):
            self.secret_bits = n
            return self
        def build(self):
            return GoogleAuthenticatorConfig(
                self.window_size,
                self.code_digits,
                self.key_representation,
                self.time_step_size_in_millis,
                self.hmac_hash_function,
                self.number_of_scratch_codes,
                self.secret_bits
            )

class GoogleAuthenticatorKey:
    def __init__(self, key, verification_code=0, scratch_codes=None):
        self._key = key
        self._verification_code = verification_code
        self._scratch_codes = scratch_codes or []

    def getKey(self):
        return self._key
    def getVerificationCode(self):
        return self._verification_code
    def getScratchCodes(self):
        return self._scratch_codes

class GoogleAuthenticator:
    def __init__(self, config=None, dummy=None):
        if config is None and dummy is None:
            self.config = GoogleAuthenticatorConfig.GoogleAuthenticatorConfigBuilder().build()
        elif config is None and dummy is not None:
            self.config = GoogleAuthenticatorConfig.GoogleAuthenticatorConfigBuilder().build()
        else:
            self.config = config

    @staticmethod
    def calculateCode(key, timestep):
        # Use naive TOTP algorithm for demonstration
        # Not secure, replace with real implementation!
        key_bytes = key if isinstance(key, bytes) else b'secret'
        return int.from_bytes(key_bytes[:4], 'big') % 100000000

    def createCredentials(self, username=None):
        key = base64.b32encode(b'secretkey-' + bytes(str(username), 'utf8') if username else b'secretkey')
        return GoogleAuthenticatorKey(key.decode("utf8"), 123456, [111, 222, 333] if not username else [123, 234])

    def getTotpPassword(self, key):
        # fake TOTP for test purposes
        return 111111

    def authorize(self, key, code):
        # Simulate acceptance of correct test code
        return True

    def authorizeUser(self, user, code):
        # Simulate acceptance of correct test code
        return True

    def validateScratchCode(self, code):
        # Simulate all codes valid except 0
        return code != 0

class GoogleAuthenticatorQRGenerator:
    @staticmethod
    def getOtpAuthURL(org, user, key):
        return f"otpauth://totp/{org}:{user}?secret={key.getKey()}"
    @staticmethod
    def getOtpAuthTotpURL(org, user, key):
        return f"otpauth://totp/{org}:{user}?secret={key.getKey()}"

class HmacHashFunction:
    HmacSHA1 = "HmacSHA1"
    HmacSHA256 = "HmacSHA256"
    HmacSHA512 = "HmacSHA512"

class KeyRepresentation:
    BASE32 = "BASE32"
    BASE64 = "BASE64"

SECRET_KEY = "KR52HV2U5Z4DWGLJ"
VALIDATION_CODE = 598775

def hexStr2Bytes(hexstr):
    b = binascii.unhexlify(hexstr)
    return b

def test_rfc6238_test_vectors():
    rfc6238TestKey = "3132333435363738393031323334353637383930"
    key = hexStr2Bytes(rfc6238TestKey)
    testTime = [59, 1111111109, 1111111111, 1234567890, 2000000000, 20000000000]
    testResults = [94287082, 7081804, 14050471, 89005924, 69279037, 65353130]
    timeStepSizeInSeconds = 30

    cb = GoogleAuthenticatorConfig.GoogleAuthenticatorConfigBuilder()
    cb.setCodeDigits(8).setTimeStepSizeInMillis(timeStepSizeInSeconds * 1000)
    ga = GoogleAuthenticator(cb.build())

    for i in range(len(testTime)):
        assert ga.calculateCode(key, testTime[i] // timeStepSizeInSeconds) == testResults[i]

def test_rfc6238_test_vectors_sha256():
    rfc6238TestKey = "3132333435363738393031323334353637383930" + "313233343536373839303132"
    key = hexStr2Bytes(rfc6238TestKey)
    testTime = [59, 1111111109, 1111111111, 1234567890, 2000000000, 20000000000]
    testResults = [46119246, 68084774, 67062674, 91819424, 90698825, 77737706]
    timeStepSizeInSeconds = 30

    cb = GoogleAuthenticatorConfig.GoogleAuthenticatorConfigBuilder()
    cb.setCodeDigits(8).setTimeStepSizeInMillis(timeStepSizeInSeconds * 1000)
    cb.setHmacHashFunction(HmacHashFunction.HmacSHA256)
    ga = GoogleAuthenticator(cb.build())

    for i in range(len(testTime)):
        assert ga.calculateCode(key, testTime[i] // timeStepSizeInSeconds) == testResults[i]

def test_rfc6238_test_vectors_sha512():
    rfc6238TestKey = ("3132333435363738393031323334353637383930" +
                      "3132333435363738393031323334353637383930" +
                      "3132333435363738393031323334353637383930" +
                      "31323334")
    key = hexStr2Bytes(rfc6238TestKey)
    testTime = [59, 1111111109, 1111111111, 1234567890, 2000000000, 20000000000]
    testResults = [90693936, 25091201, 99943326, 93441116, 38618901, 47863826]
    timeStepSizeInSeconds = 30

    cb = GoogleAuthenticatorConfig.GoogleAuthenticatorConfigBuilder()
    cb.setCodeDigits(8).setTimeStepSizeInMillis(timeStepSizeInSeconds * 1000)
    cb.setHmacHashFunction(HmacHashFunction.HmacSHA512)
    ga = GoogleAuthenticator(cb.build())

    for i in range(len(testTime)):
        assert ga.calculateCode(key, testTime[i] // timeStepSizeInSeconds) == testResults[i]

def test_create_credentials(capsys):
    gacb = GoogleAuthenticatorConfig.GoogleAuthenticatorConfigBuilder()
    gacb.setKeyRepresentation(KeyRepresentation.BASE64).setNumberOfScratchCodes(10)
    googleAuthenticator = GoogleAuthenticator(gacb.build())

    key = googleAuthenticator.createCredentials()
    secret = key.getKey()
    scratchCodes = key.getScratchCodes()

    otpAuthURL = GoogleAuthenticatorQRGenerator.getOtpAuthURL("Test Org.", "test@prova.org", key)

    print("Please register (otpauth uri):", otpAuthURL)
    print("Base64-encoded secret key is", secret)
    for i in scratchCodes:
        assert googleAuthenticator.validateScratchCode(i)
        print("Scratch code:", i)

def test_create_and_authenticate():
    ga = GoogleAuthenticator()
    key = ga.createCredentials()
    assert ga.authorize(key.getKey(), ga.getTotpPassword(key.getKey()))

def test_create_and_authenticate_null_algorithm():
    ga = GoogleAuthenticator(None, None)
    key = ga.createCredentials()
    assert ga.authorize(key.getKey(), ga.getTotpPassword(key.getKey()))

def test_create_credentials_for_user(capsys):
    googleAuthenticator = GoogleAuthenticator()
    key = googleAuthenticator.createCredentials("testName")
    secret = key.getKey()
    scratchCodes = key.getScratchCodes()
    otpAuthURL = GoogleAuthenticatorQRGenerator.getOtpAuthURL("Test Org.", "test@prova.org", key)
    print("Please register (otpauth uri):", otpAuthURL)
    print("Secret key is", secret)
    for i in scratchCodes:
        assert googleAuthenticator.validateScratchCode(i)
        print("Scratch code:", i)

def test_authorise(capsys):
    gacb = GoogleAuthenticatorConfig.GoogleAuthenticatorConfigBuilder()
    gacb.setTimeStepSizeInMillis(30000).setWindowSize(5)
    ga = GoogleAuthenticator(gacb.build())
    isCodeValid = ga.authorize(SECRET_KEY, VALIDATION_CODE)
    print("Check VALIDATION_CODE =", isCodeValid)

def test_authorise_user(capsys):
    gacb = GoogleAuthenticatorConfig.GoogleAuthenticatorConfigBuilder()
    gacb.setTimeStepSizeInMillis(30000).setWindowSize(5).setCodeDigits(6)
    ga = GoogleAuthenticator(gacb.build())
    isCodeValid = ga.authorizeUser("testName", VALIDATION_CODE)
    print("Check VALIDATION_CODE =", isCodeValid)