package original

import "testing"

type Pyzbar struct {
	Version string
}

func TestVersionExists(t *testing.T) {
	pyz := Pyzbar{Version: "1.0.0"}
	if pyz.Version == "" {
		t.Error("expected version attribute to exist and be string")
	}
}