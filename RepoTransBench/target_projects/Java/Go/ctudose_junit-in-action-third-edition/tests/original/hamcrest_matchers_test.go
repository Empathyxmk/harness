package original

import (
	"testing"
	"reflect"
)

type Customer struct {
	FirstName string
	LastName  string
}

func TestHamcrestIs(t *testing.T) {
	price1, price2, price3 := 1, 1, 2
	if 1 != price1 {
		t.Errorf("expected 1 == price1, got %d", price1)
	}
	if (1 != price2) && (1 != price3) {
		t.Errorf("expected 1 to be equal to either price2 or price3; got %d, %d", price2, price3)
	}
	if !(1 == price1 && 1 == price2) {
		t.Errorf("expected allOf: 1 == price1 && 1 == price2, got %d, %d", price1, price2)
	}
}

func TestNull(t *testing.T) {
	var v interface{}
	if v != nil {
		t.Errorf("v should be nil, got %v", v)
	}
}

func TestNotNull(t *testing.T) {
	customer := &Customer{"John", "Smith"}
	if customer == nil {
		t.Error("customer should not be nil")
	}
}

func TestCorrectCustomerProperties(t *testing.T) {
	FIRST_NAME := "John"
	LAST_NAME := "Smith"
	customer := &Customer{FIRST_NAME, LAST_NAME}
	val := reflect.ValueOf(*customer)
	first := val.FieldByName("FirstName")
	last := val.FieldByName("LastName")
	if first.String() != FIRST_NAME {
		t.Errorf("expected FirstName to be %s, got %s", FIRST_NAME, first.String())
	}
	if last.String() != LAST_NAME {
		t.Errorf("expected LastName to be %s, got %s", LAST_NAME, last.String())
	}
}