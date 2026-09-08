package public_tests

import (
	"testing"
)

type BundlePublic map[string]interface{}

type PublicTestBundler struct{}

func (b *PublicTestBundler) Put(key string, value string, bundle BundlePublic) {
	bundle[key] = "PUBLIC_" + value + "_PUBTEST"
}

func (b *PublicTestBundler) Get(key string, bundle BundlePublic) string {
	v, ok := bundle[key].(string)
	if !ok {
		return ""
	}
	return stripPrefixSuffix(v)
}

func stripPrefixSuffix(val string) string {
	if len(val) >= 14 && val[:7] == "PUBLIC_" && val[len(val)-8:] == "_PUBTEST" {
		return val[7 : len(val)-8]
	}
	return val
}

func TestInterfacePutAddsPrefixSuffixPublic(t *testing.T) {
	bundle := BundlePublic{}
	(&PublicTestBundler{}).Put("PUBKEY", "valueForPublic", bundle)
	expected := "PUBLIC_valueForPublic_PUBTEST"
	if bundle["PUBKEY"] != expected {
		t.Errorf("Expected %q, got %q", expected, bundle["PUBKEY"])
	}
}

func TestInterfaceGetRemovesPrefixSuffixPublic(t *testing.T) {
	bundle := BundlePublic{"PUB_KEY": "PUBLIC_zxy_PUBTEST"}
	got := (&PublicTestBundler{}).Get("PUB_KEY", bundle)
	if got != "zxy" {
		t.Errorf("Expected \"zxy\", got %q", got)
	}
}