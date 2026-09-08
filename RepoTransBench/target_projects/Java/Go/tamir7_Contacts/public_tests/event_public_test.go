package public_tests

import (
	"testing"

	"github.com/tamir7/contacts"
)

func TestEventPublic_ConstructorsAndGetters_Type(t *testing.T) {
	e := contacts.NewEventWithType("2050-12-31", contacts.EventTypeANNIVERSARY)
	if e.StartDate != "2050-12-31" {
		t.Errorf("expected 2050-12-31, got %v", e.StartDate)
	}
	if e.Type != contacts.EventTypeANNIVERSARY {
		t.Errorf("expected ANNIVERSARY, got %v", e.Type)
	}
	if e.Label != "" {
		t.Errorf("expected empty label, got %v", e.Label)
	}
}

func TestEventPublic_ConstructorsAndGetters_Label(t *testing.T) {
	e := contacts.NewEventWithLabel("2024-07-14", "Special Date")
	if e.StartDate != "2024-07-14" {
		t.Errorf("expected 2024-07-14, got %v", e.StartDate)
	}
	if e.Type != contacts.EventTypeCUSTOM {
		t.Errorf("expected type CUSTOM, got %v", e.Type)
	}
	if e.Label != "Special Date" {
		t.Errorf("expected label 'Special Date', got %v", e.Label)
	}
}

func TestEventPublic_EqualsAndHashCode(t *testing.T) {
	e1 := contacts.NewEventWithType("2000-01-01", contacts.EventTypeOTHER)
	e2 := contacts.NewEventWithType("2000-01-01", contacts.EventTypeOTHER)
	e3 := contacts.NewEventWithLabel("2000-01-01", "Anniv")
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

func TestEventPublic_TypeFromValue(t *testing.T) {
	if contacts.EventTypeFromValue(-1) != contacts.EventTypeCUSTOM {
		t.Errorf("expected -1 -> CUSTOM")
	}
	if contacts.EventTypeFromValue(1) != contacts.EventTypeANNIVERSARY {
		t.Errorf("expected 1 -> ANNIVERSARY")
	}
	if contacts.EventTypeFromValue(2) != contacts.EventTypeOTHER {
		t.Errorf("expected 2 -> OTHER")
	}
	if contacts.EventTypeFromValue(3) != contacts.EventTypeBIRTHDAY {
		t.Errorf("expected 3 -> BIRTHDAY")
	}
	if contacts.EventTypeFromValue(500) != contacts.EventTypeUNKNOWN {
		t.Errorf("expected 500 -> UNKNOWN")
	}
}

func TestEventPublic_NotEqualConditions(t *testing.T) {
	e1 := contacts.NewEventWithType("2029-11-11", contacts.EventTypeOTHER)
	if e1.Equal(nil) {
		t.Errorf("should not equal nil")
	}
	if e1.Equal(struct{}{}) {
		t.Errorf("should not equal arbitrary type")
	}
	e2 := contacts.NewEventWithType("2222-02-22", contacts.EventTypeOTHER)
	if e1.Equal(e2) {
		t.Errorf("should not equal a different event")
	}
}