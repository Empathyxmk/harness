package original

import (
	"testing"
	"github.com/tamir7/contacts"
)

func TestEmail_ConstructorsAndGetters_Type(t *testing.T) {
	e := contacts.NewEmailWithType("addr@email.com", contacts.EmailTypeWORK)
	if e.Address != "addr@email.com" {
		t.Errorf("expected address to be 'addr@email.com', got %v", e.Address)
	}
	if e.Type != contacts.EmailTypeWORK {
		t.Errorf("expected type to be WORK, got %v", e.Type)
	}
	if e.Label != "" {
		t.Errorf("expected label to be empty, got %v", e.Label)
	}
}

func TestEmail_ConstructorsAndGetters_Label(t *testing.T) {
	e := contacts.NewEmailWithLabel("foo@bar.com", "mylabel")
	if e.Address != "foo@bar.com" {
		t.Errorf("expected address 'foo@bar.com', got %v", e.Address)
	}
	if e.Type != contacts.EmailTypeCUSTOM {
		t.Errorf("expected type CUSTOM, got %v", e.Type)
	}
	if e.Label != "mylabel" {
		t.Errorf("expected label 'mylabel', got %v", e.Label)
	}
}

func TestEmail_EqualsAndHashCode(t *testing.T) {
	e1 := contacts.NewEmailWithType("x@x.com", contacts.EmailTypeHOME)
	e2 := contacts.NewEmailWithType("x@x.com", contacts.EmailTypeHOME)
	e3 := contacts.NewEmailWithLabel("x@x.com", "label")
	if !e1.Equal(e2) {
		t.Errorf("expected e1 == e2")
	}
	if e1.Equal(e3) {
		t.Errorf("expected e1 != e3")
	}
	if e1.HashCode() != e2.HashCode() {
		t.Errorf("expected hash codes to match")
	}
}

func TestEmail_TypeFromValue(t *testing.T) {
	if contacts.EmailTypeFromValue(0) != contacts.EmailTypeCUSTOM {
		t.Errorf("expected 0 to map to CUSTOM")
	}
	if contacts.EmailTypeFromValue(1) != contacts.EmailTypeHOME {
		t.Errorf("expected 1 to map to HOME")
	}
	if contacts.EmailTypeFromValue(2) != contacts.EmailTypeWORK {
		t.Errorf("expected 2 to map to WORK")
	}
	if contacts.EmailTypeFromValue(3) != contacts.EmailTypeOTHER {
		t.Errorf("expected 3 to map to OTHER")
	}
	if contacts.EmailTypeFromValue(4) != contacts.EmailTypeMOBILE {
		t.Errorf("expected 4 to map to MOBILE")
	}
	if contacts.EmailTypeFromValue(99) != contacts.EmailTypeUNKNOWN {
		t.Errorf("expected 99 to map to UNKNOWN")
	}
}

func TestEmail_NotEqualConditions(t *testing.T) {
	e1 := contacts.NewEmailWithType("x@x.com", contacts.EmailTypeHOME)
	if e1.Equal(nil) {
		t.Errorf("should not be equal to nil")
	}
	if e1.Equal("notAnEmail") {
		t.Errorf("should not be equal to non-Email types")
	}
	e2 := contacts.NewEmailWithType("z@z.com", contacts.EmailTypeHOME)
	if e1.Equal(e2) {
		t.Errorf("should not be equal to different email")
	}
}