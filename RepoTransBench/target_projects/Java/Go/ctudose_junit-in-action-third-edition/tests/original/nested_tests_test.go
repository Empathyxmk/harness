package original

import (
	"testing"
	"time"
	"reflect"
)

type Gender string
const (
	MALE   Gender = "MALE"
	FEMALE Gender = "FEMALE"
)

// Nested builder struct for Customer
type Customer struct {
	Gender         Gender
	FirstName      string
	LastName       string
	MiddleName     string
	BecomeCustomer time.Time
}

type CustomerBuilder struct {
	cust *Customer
}

func NewCustomerBuilder(g Gender, first, last string) *CustomerBuilder {
	return &CustomerBuilder{
		cust: &Customer{Gender: g, FirstName: first, LastName: last},
	}
}
func (b *CustomerBuilder) WithMiddleName(m string) *CustomerBuilder {
	b.cust.MiddleName = m
	return b
}
func (b *CustomerBuilder) WithBecomeCustomer(t time.Time) *CustomerBuilder {
	b.cust.BecomeCustomer = t
	return b
}
func (b *CustomerBuilder) Build() *Customer {
	return b.cust
}

func customersAreEqual(a, b *Customer) bool {
	return a.Gender == b.Gender &&
		a.FirstName == b.FirstName &&
		a.LastName == b.LastName &&
		a.MiddleName == b.MiddleName &&
		a.BecomeCustomer.Equal(b.BecomeCustomer)
}

func TestCustomerBuilder(t *testing.T) {
	const FIRST_NAME = "John"
	const LAST_NAME = "Smith"
	const MIDDLE_NAME = "Michael"
	layout := "01-02-2006"
	customerDate, _ := time.Parse(layout, "04-21-2019")
	builder := NewCustomerBuilder(MALE, FIRST_NAME, LAST_NAME).
		WithMiddleName(MIDDLE_NAME).
		WithBecomeCustomer(customerDate)
	customer := builder.Build()
	if customer.Gender != MALE ||
		customer.FirstName != FIRST_NAME ||
		customer.LastName != LAST_NAME ||
		customer.MiddleName != MIDDLE_NAME ||
		!customer.BecomeCustomer.Equal(customerDate) {
		t.Error("Customer builder values do not match expected")
	}
}

func TestCustomerDifferent(t *testing.T) {
	const FIRST_NAME, LAST_NAME = "John", "Smith"
	const OTHER_FIRST_NAME, OTHER_LAST_NAME = "John", "Doe"
	c1 := NewCustomerBuilder(MALE, FIRST_NAME, LAST_NAME).Build()
	c2 := NewCustomerBuilder(MALE, OTHER_FIRST_NAME, OTHER_LAST_NAME).Build()
	if reflect.DeepEqual(c1, c2) {
		t.Error("Expected customers to NOT be equal, but got equal")
	}
}

func TestCustomerSame(t *testing.T) {
	const FIRST_NAME, LAST_NAME = "John", "Smith"
	c1 := NewCustomerBuilder(MALE, FIRST_NAME, LAST_NAME).Build()
	c2 := NewCustomerBuilder(MALE, FIRST_NAME, LAST_NAME).Build()
	if !reflect.DeepEqual(c1, c2) {
		t.Error("Expected customers to be equal")
	}
	if c1 == c2 {
		t.Error("Expected not the same pointer")
	}
}

func TestCustomerHashCodeDifferent(t *testing.T) {
	const FIRST_NAME, LAST_NAME = "John", "Smith"
	const OTHER_FIRST_NAME, OTHER_LAST_NAME = "John", "Doe"
	c1 := NewCustomerBuilder(MALE, FIRST_NAME, LAST_NAME).Build()
	c2 := NewCustomerBuilder(MALE, OTHER_FIRST_NAME, OTHER_LAST_NAME).Build()
	if hashCustomer(c1) == hashCustomer(c2) {
		t.Error("Expected different hashcodes")
	}
}

func TestCustomerHashCodeSame(t *testing.T) {
	const FIRST_NAME, LAST_NAME = "John", "Smith"
	c1 := NewCustomerBuilder(MALE, FIRST_NAME, LAST_NAME).Build()
	c2 := NewCustomerBuilder(MALE, FIRST_NAME, LAST_NAME).Build()
	if hashCustomer(c1) != hashCustomer(c2) {
		t.Error("Expected same hashcodes for identical customers")
	}
}

func hashCustomer(c *Customer) int {
	// basic hash based on values
	v := c.FirstName + "|" + c.LastName + "|" + c.MiddleName + "|" + c.Gender + "|" + c.BecomeCustomer.String()
	h := 0
	for i := 0; i < len(v); i++ {
		h = h*31 + int(v[i])
	}
	return h
}