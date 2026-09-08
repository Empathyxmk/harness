package public_tests

import "testing"

type PublicMountain struct{}

func (m *PublicMountain) SomeMethod() {}

func TestPublicMountainHasClass(t *testing.T) {
	m := PublicMountain{}
	if m != (PublicMountain{}) {
		t.Error("Should be able to construct mountain")
	}
}

func TestPublicMountainHasMethods(t *testing.T) {
	m := PublicMountain{}
	found := false
	// Go: check for any method via interface
	type iface interface {
		SomeMethod()
	}
	ifaceVal, ok := interface{}(&m).(iface)
	if ok && ifaceVal != nil {
		found = true
	}
	if !found {
		t.Error("Should be able to find a Mountain method")
	}
}