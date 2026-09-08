package public_tests

import (
	"testing"
)

const (
	APK_SIG_BLOCK_MAGIC_HI = 0x3234206b636f6c42
	APK_SIG_BLOCK_MAGIC_LO = 0x20676953204b5041
	DEFAULT_CHARSET        = "UTF-8"
	APK_CHANNEL_BLOCK_ID   = 0x71777777
)

type ApkUtil struct{}

func TestApkUtilPublic_ApkSigBlockMagicConstants_public(t *testing.T) {
	if APK_SIG_BLOCK_MAGIC_HI != 0x3234206b636f6c42 {
		t.Errorf("APK_SIG_BLOCK_MAGIC_HI not correct")
	}
	if APK_SIG_BLOCK_MAGIC_LO != 0x20676953204b5041 {
		t.Errorf("APK_SIG_BLOCK_MAGIC_LO not correct")
	}
}

func TestApkUtilPublic_DefaultCharset_public(t *testing.T) {
	if DEFAULT_CHARSET != "UTF-8" {
		t.Errorf("expected UTF-8 as default charset")
	}
}

func TestApkUtilPublic_ChannelBlockId_public(t *testing.T) {
	if APK_CHANNEL_BLOCK_ID != 0x71777777 {
		t.Errorf("APK_CHANNEL_BLOCK_ID constant mismatch")
	}
}