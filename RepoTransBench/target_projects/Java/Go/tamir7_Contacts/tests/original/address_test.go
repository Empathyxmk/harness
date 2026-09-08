package original

import (
	"testing"
	"github.com/tamir7/contacts"
)

func TestAddress_GettersAndConstructors_Type(t *testing.T) {
	a := contacts.NewAddressWithType("addr", "str", "city", "reg", "zip", "country", contacts.AddressTypeHOME)
	if a.FormattedAddress != "addr" {
		t.Errorf("expected formatted address %v, got %v", "addr", a.FormattedAddress)
	}
	if a.Street != "str" {
		t.Errorf("expected street 'str', got %v", a.Street)
	}
	if a.City != "city" {
		t.Errorf("expected city 'city', got %v", a.City)
	}
	if a.Region != "reg" {
		t.Errorf("expected region 'reg', got %v", a.Region)
	}
	if a.Postcode != "zip" {
		t.Errorf("expected postcode 'zip', got %v", a.Postcode)
	}
	if a.Country != "country" {
		t.Errorf("expected country 'country', got %v", a.Country)
	}
	if a.Label != "" {
		t.Errorf("expected label empty, got %v", a.Label)
	}
	if a.Type != contacts.AddressTypeHOME {
		t.Errorf("expected type HOME, got %v", a.Type)
	}
}

func TestAddress_GettersAndConstructors_Label(t *testing.T) {
	a := contacts.NewAddressWithLabel("addr", "str", "city", "reg", "zip", "country", "myLabel")
	if a.Label != "myLabel" {
		t.Errorf("expected label 'myLabel', got %v", a.Label)
	}
	if a.Type != contacts.AddressTypeCUSTOM {
		t.Errorf("expected type CUSTOM, got %v", a.Type)
	}
}

func TestAddress_TypeFromValue(t *testing.T) {
	if contacts.AddressTypeFromValue(0) != contacts.AddressTypeCUSTOM {
		t.Errorf("expected 0->CUSTOM")
	}
	if contacts.AddressTypeFromValue(1) != contacts.AddressTypeHOME {
		t.Errorf("expected 1->HOME")
	}
	if contacts.AddressTypeFromValue(2) != contacts.AddressTypeWORK {
		t.Errorf("expected 2->WORK")
	}
	if contacts.AddressTypeFromValue(3) != contacts.AddressTypeOTHER {
		t.Errorf("expected 3->OTHER")
	}
	if contacts.AddressTypeFromValue(99) != contacts.AddressTypeUNKNOWN {
		t.Errorf("expected 99->UNKNOWN")
	}
}