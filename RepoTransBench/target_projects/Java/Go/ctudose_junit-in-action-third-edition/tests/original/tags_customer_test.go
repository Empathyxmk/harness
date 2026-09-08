package original

import (
	"testing"
)

type Customer struct {
	Name string
}

func TestCustomer(t *testing.T) {
	customer := &Customer{"John Smith"}
	if customer.Name != "John Smith" {
		t.Errorf("expected customer name %s, got %s", "John Smith", customer.Name)
	}
}