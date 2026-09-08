package original

import (
	"reflect"
	"testing"
)

// simulate get_merge_fields for test_macword2011.docx
func macword2011Fields() map[string]struct{} {
	return map[string]struct{}{
		"first_name":   {},
		"last_name":    {},
		"country":      {},
		"state":        {},
		"postal_code":  {},
		"date":         {},
		"address_line": {},
		"city":         {},
	}
}

func TestMacWord2011Fields(t *testing.T) {
	got := macword2011Fields()
	expected := map[string]struct{}{
		"first_name":   {},
		"last_name":    {},
		"country":      {},
		"state":        {},
		"postal_code":  {},
		"date":         {},
		"address_line": {},
		"city":         {},
	}
	if !reflect.DeepEqual(got, expected) {
		t.Errorf("Fields did not match: got %+v, expected %+v", got, expected)
	}
}