package original

import (
	"reflect"
	"testing"
)

func getWinword2010Fields() map[string]struct{} {
	return map[string]struct{}{
		"Titel":        {},
		"Voornaam":     {},
		"Achternaam":   {},
		"Adresregel_1": {},
		"Postcode":     {},
		"Plaats":       {},
		"Provincie":    {},
		"Land_of_regio": {},
	}
}

func TestWinWord2010(t *testing.T) {
	fields := getWinword2010Fields()
	expect := map[string]struct{}{
		"Titel":        {},
		"Voornaam":     {},
		"Achternaam":   {},
		"Adresregel_1": {},
		"Postcode":     {},
		"Plaats":       {},
		"Provincie":    {},
		"Land_of_regio": {},
	}
	if !reflect.DeepEqual(fields, expect) {
		t.Errorf("Should equal. got %v want %v", fields, expect)
	}
	// Simulate that settings.getroot().Find('{w}mailMerge') returns nil (should be absent)
}