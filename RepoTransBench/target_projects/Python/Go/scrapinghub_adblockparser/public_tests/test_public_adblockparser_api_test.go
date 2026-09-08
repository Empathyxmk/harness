package public_tests

import (
	"reflect"
	"testing"

	"scrapinghub_adblockparser/adblockparser"
)

func TestPublicImportsAvailable(t *testing.T) {
	if reflect.ValueOf(adblockparser.AdblockParsingError).IsNil() {
		t.Errorf("AdblockParsingError is not present")
	}
	_ = adblockparser.NewAdblockRule("")
	_ = adblockparser.NewAdblockRules([]string{})
}