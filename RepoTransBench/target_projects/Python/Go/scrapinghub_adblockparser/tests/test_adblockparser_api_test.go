package tests

import (
	"reflect"
	"testing"

	"scrapinghub_adblockparser/adblockparser"
)

func TestImportsAvailable(t *testing.T) {
	if reflect.ValueOf(adblockparser.AdblockParsingError).IsNil() {
		t.Errorf("AdblockParsingError is not present")
	}
	_ = adblockparser.NewAdblockRule("")
	_ = adblockparser.NewAdblockRules([]string{})
}