package public_tests

import (
	"testing"

	"github.com/tamir7/contacts"
)

func TestEmailPublic_ConstructorsAndGetters_Type(t *testing.T) {
	e := contacts.NewEmailWithType("test@public.com", contacts.EmailTypeHOME)
	if e.Address != "test@public.com" {
		t.Errorf("expected 'test@public.com', got %v", e.Address)
	}
	if e.Type != contacts.EmailTypeHOME {
		t.Errorf("expected HOME, got %v", e.Type)
	}
	if e.Label != "" {
		t.Errorf("expected empty label, got %v", e.Label)
	}
}

func TestEmailPublic_ConstructorsAndGetters_Label(t *testing.T) {
	e := contacts.NewEmailWithLabel("alpha@beta.com", "office")
	if e.Address != "alpha@beta.com" {
		t.Errorf("expected alpha@beta.com, got %v", e.Address)
	}
	if e.Type != contacts.EmailTypeCUSTOM {
		t.Errorf("expected CUSTOM, got %v", e.Type)
	}
	if e.Label != "office" {
		t.Errorf("expected label office, got %v", e.Label)
	}
}

func TestEmailPublic_EqualsAndHashCode(t *testing.T) {
	e1 := contacts.NewEmailWithType("unique@mail.com", contacts.EmailTypeMOBILE)
	e2 := contacts.NewEmailWithType("unique@mail.com", contacts.EmailTypeMOBILE)
	e3 := contacts.NewEmailWithLabel("unique@mail.com", "project")
	if !e1.Equal(e2) {
		t.Errorf("expected e1 == e2")
	}
	if e1.Equal(e3) {
		t.Errorf("expected e1 != e3")
	}
	if e1.HashCode() != e2.HashCode() {
		t.Errorf("expected hashcode match")
	}
}

func TestEmailPublic_TypeFromValue(t *testing.T) {
	if contacts.EmailTypeFromValue(-1) != contacts.EmailTypeCUSTOM {
		t.Errorf("expected -1 -> CUSTOM")
	}
	if contacts.EmailTypeFromValue(1) != contacts.EmailTypeHOME {
		t.Errorf("expected 1 -> HOME")
	}
	if contacts.EmailTypeFromValue(2) != contacts.EmailTypeWORK {
		t.Errorf("expected 2 -> WORK")
	}
	if contacts.EmailTypeFromValue(3) != contacts.EmailTypeOTHER {
		t.Errorf("expected 3 -> OTHER")
	}
	if contacts.EmailTypeFromValue(4) != contacts.EmailTypeMOBILE {
		t.Errorf("expected 4 -> MOBILE")
	}
	if contacts.EmailTypeFromValue(123) != contacts.EmailTypeUNKNOWN {
		t.Errorf("expected 123 -> UNKNOWN")
	}
}

func TestEmailPublic_NotEqualConditions(t *testing.T) {
	e1 := contacts.NewEmailWithType("nobody@nowhere.com", contacts.EmailTypeMOBILE)
	if e1.Equal(nil) {
		t.Errorf("should not equal nil")
	}
	if e1.Equal("NotAnEmailObject") {
		t.Errorf("should not equal arbitrary type")
	}
	e2 := contacts.NewEmailWithType("someone@somewhere.com", contacts.EmailTypeMOBILE)
	if e1.Equal(e2) {
		t.Errorf("should not equal a different object")
	}
}