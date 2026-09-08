package original

import (
	"testing"
	"github.com/tamir7/contacts"
)

func TestEvent_ConstructorsAndGetters_Type(t *testing.T) {
	e := contacts.NewEventWithType("2023-01-01", contacts.EventTypeBIRTHDAY)
	if e.StartDate != "2023-01-01" {
		t.Errorf("expected startDate '2023-01-01', got %v", e.StartDate)
	}
	if e.Type != contacts.EventTypeBIRTHDAY {
		t.Errorf("expected type BIRTHDAY, got %v", e.Type)
	}
	if e.Label != "" {
		t.Errorf("expected label empty, got %v", e.Label)
	}
}

func TestEvent_ConstructorsAndGetters_Label(t *testing.T) {
	e := contacts.NewEventWithLabel("2023-01-01", "Anniversary")
	if e.StartDate != "2023-01-01" {
		t.Errorf("expected '2023-01-01', got %v", e.StartDate)
	}
	if e.Type != contacts.EventTypeCUSTOM {
		t.Errorf("expected type CUSTOM, got %v", e.Type)
	}
	if e.Label != "Anniversary" {
		t.Errorf("expected label Anniversary, got %v", e.Label)
	}
}

func TestEvent_EqualsAndHashCode(t *testing.T) {
	e1 := contacts.NewEventWithType("2020-10-10", contacts.EventTypeBIRTHDAY)
	e2 := contacts.NewEventWithType("2020-10-10", contacts.EventTypeBIRTHDAY)
	e3 := contacts.NewEventWithLabel("2020-10-10", "CustomEvt")
	if !e1.Equal(e2) {
		t.Errorf("expected e1 == e2")
	}
	if e1.Equal(e3) {
		t.Errorf("expected e1 != e3")
	}
	if e1.HashCode() != e2.HashCode() {
		t.Errorf("hashcodes should match")
	}
}

func TestEvent_TypeFromValue(t *testing.T) {
	if contacts.EventTypeFromValue(0) != contacts.EventTypeCUSTOM {
		t.Errorf("expected 0->CUSTOM")
	}
	if contacts.EventTypeFromValue(1) != contacts.EventTypeANNIVERSARY {
		t.Errorf("expected 1->ANNIVERSARY")
	}
	if contacts.EventTypeFromValue(2) != contacts.EventTypeOTHER {
		t.Errorf("expected 2->OTHER")
	}
	if contacts.EventTypeFromValue(3) != contacts.EventTypeBIRTHDAY {
		t.Errorf("expected 3->BIRTHDAY")
	}
	if contacts.EventTypeFromValue(99) != contacts.EventTypeUNKNOWN {
		t.Errorf("expected 99->UNKNOWN")
	}
}

func TestEvent_NotEqualConditions(t *testing.T) {
	e1 := contacts.NewEventWithType("d", contacts.EventTypeBIRTHDAY)
	if e1.Equal(nil) {
		t.Errorf("should not equal nil")
	}
	if e1.Equal("notAnEvent") {
		t.Errorf("should not equal a string")
	}
	e2 := contacts.NewEventWithType("other", contacts.EventTypeBIRTHDAY)
	if e1.Equal(e2) {
		t.Errorf("should not equal another event with different StartDate")
	}
}