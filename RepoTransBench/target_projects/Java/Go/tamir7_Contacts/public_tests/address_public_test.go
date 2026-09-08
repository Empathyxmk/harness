package public_tests

import (
	"testing"
	"github.com/tamir7/contacts"
)

func TestAddressPublic_ConstructorsAndGetters_Type(t *testing.T) {
	a := contacts.NewAddressWithType("Street 123", "Townsville", "AA", "CountryX", "98765", "", contacts.AddressTypeWORK)
	if a.Street != "Street 123" {
		t.Errorf("expected Street 123, got %v", a.Street)
	}
	if a.City != "Townsville" {
		t.Errorf("expected Townsville, got %v", a.City)
	}
	if a.Region != "AA" {
		t.Errorf("expected AA, got %v", a.Region)
	}
	if a.Country != "CountryX" {
		t.Errorf("expected CountryX, got %v", a.Country)
	}
	if a.Postcode != "98765" {
		t.Errorf("expected 98765, got %v", a.Postcode)
	}
	if a.Type != contacts.AddressTypeWORK {
		t.Errorf("expected WORK, got %v", a.Type)
	}
	if a.Label != "" {
		t.Errorf("expected empty label, got %v", a.Label)
	}
}

func TestAddressPublic_ConstructorsAndGetters_Label(t *testing.T) {
	a := contacts.NewAddressWithLabel("Ave A", "Metropolis", "BB", "CountryY", "24680", "Vacation Spot")
	if a.Street != "Ave A" {
		t.Errorf("expected Ave A, got %v", a.Street)
	}
	if a.City != "Metropolis" {
		t.Errorf("expected Metropolis, got %v", a.City)
	}
	if a.Region != "BB" {
		t.Errorf("expected BB, got %v", a.Region)
	}
	if a.Country != "CountryY" {
		t.Errorf("expected CountryY, got %v", a.Country)
	}
	if a.Postcode != "24680" {
		t.Errorf("expected 24680, got %v", a.Postcode)
	}
	if a.Type != contacts.AddressTypeCUSTOM {
		t.Errorf("expected type CUSTOM, got %v", a.Type)
	}
	if a.Label != "Vacation Spot" {
		t.Errorf("expected 'Vacation Spot', got %v", a.Label)
	}
}

func TestAddressPublic_EqualsAndHashCode(t *testing.T) {
	a1 := contacts.NewAddressWithType("Zebra", "CityZ", "RR", "LandQ", "65432", "", contacts.AddressTypeHOME)
	a2 := contacts.NewAddressWithType("Zebra", "CityZ", "RR", "LandQ", "65432", "", contacts.AddressTypeHOME)
	a3 := contacts.NewAddressWithLabel("Zebra", "CityZ", "RR", "LandQ", "65432", "MyPlace")
	if !a1.Equal(a2) {
		t.Errorf("expected a1 == a2")
	}
	if a1.Equal(a3) {
		t.Errorf("expected a1 != a3")
	}
	if a1.HashCode() != a2.HashCode() {
		t.Errorf("expected hashcode match")
	}
}

func TestAddressPublic_TypeFromValue(t *testing.T) {
	if contacts.AddressTypeFromValue(-1) != contacts.AddressTypeCUSTOM {
		t.Errorf("expected -1 -> CUSTOM")
	}
	if contacts.AddressTypeFromValue(1) != contacts.AddressTypeHOME {
		t.Errorf("expected 1 -> HOME")
	}
	if contacts.AddressTypeFromValue(2) != contacts.AddressTypeWORK {
		t.Errorf("expected 2 -> WORK")
	}
	if contacts.AddressTypeFromValue(3) != contacts.AddressTypeOTHER {
		t.Errorf("expected 3 -> OTHER")
	}
	if contacts.AddressTypeFromValue(100) != contacts.AddressTypeUNKNOWN {
		t.Errorf("expected 100 -> UNKNOWN")
	}
}

func TestAddressPublic_NotEqualConditions(t *testing.T) {
	a1 := contacts.NewAddressWithType("Alpha", "Beta", "Gamma", "Delta", "61616", "", contacts.AddressTypeWORK)
	if a1.Equal(nil) {
		t.Errorf("should not equal nil")
	}
	if a1.Equal("NotAnAddress") {
		t.Errorf("should not equal a string")
	}
	a2 := contacts.NewAddressWithType("Beta", "Gamma", "Delta", "Epsilon", "89898", "", contacts.AddressTypeWORK)
	if a1.Equal(a2) {
		t.Errorf("should not equal a different address")
	}
}