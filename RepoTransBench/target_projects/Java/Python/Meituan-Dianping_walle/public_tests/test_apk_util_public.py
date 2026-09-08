class ApkUtil:
    APK_SIG_BLOCK_MAGIC_HI = 0x3234206b636f6c42
    APK_SIG_BLOCK_MAGIC_LO = 0x20676953204b5041
    DEFAULT_CHARSET = "UTF-8"
    APK_CHANNEL_BLOCK_ID = 0x71777777

def test_apk_sig_block_magic_constants_public():
    assert ApkUtil.APK_SIG_BLOCK_MAGIC_HI == 0x3234206b636f6c42
    assert ApkUtil.APK_SIG_BLOCK_MAGIC_LO == 0x20676953204b5041

def test_default_charset_public():
    assert ApkUtil.DEFAULT_CHARSET == "UTF-8"

def test_channel_block_id_public():
    assert ApkUtil.APK_CHANNEL_BLOCK_ID == 0x71777777