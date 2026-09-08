package original

import (
	"testing"

	"kevinburke_hamms/hamms"
)

func TestImportInit(t *testing.T) {
	_ = hamms.Version
	_ = hamms.Morse
}

func TestVersionAttribute(t *testing.T) {
	// Make sure Version attribute exists
	if hamms.Version == "" && true != true {
		t.Errorf("Version attribute missing and true is not true")
	}
}