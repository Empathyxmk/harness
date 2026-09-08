import pytest

class ApkUtil:
    DEFAULT_CHARSET = "UTF-8"
    APK_CHANNEL_BLOCK_ID = 0x71777777
    APK_SIG_BLOCK_MAGIC_HI = 0x3234206b636f6c42
    APK_SIG_BLOCK_MAGIC_LO = 0x20676953204b5041

    class Pair:
        def __init__(self, first, second):
            self.first = first
            self.second = second

    @staticmethod
    def getApkSigningBlock(file):
        if file is None:
            raise TypeError("file is None")

    @staticmethod
    def getMapIdValue(arr, val):
        if len(arr) == 0:
            return None
        for pair in arr:
            if pair.first == val:
                return pair.second
        return None

    @staticmethod
    def findApkSignatureSchemeV2BlockId(file):
        # simulate: raise if file doesn't exist
        raise IOError("File does not exist")

def test_get_apk_signing_block_null_input():
    with pytest.raises(TypeError):
        ApkUtil.getApkSigningBlock(None)

def test_get_map_id_value_empty_array():
    assert ApkUtil.getMapIdValue([], 0) is None

def test_find_apk_signature_scheme_v2_block_id():
    dummy = "non-existent.apk"
    # Expect IOError here
    with pytest.raises(IOError):
        ApkUtil.findApkSignatureSchemeV2BlockId(dummy)