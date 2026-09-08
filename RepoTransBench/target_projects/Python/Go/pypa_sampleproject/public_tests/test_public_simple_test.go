package public_tests

import (
	"testing"
	"pypa_sampleproject/src/sample"
)

func TestAddOneLargePositive(t *testing.T) {
	got := sample.AddOne(100)
	want := 101
	if got != want {
		t.Errorf("AddOne(100) = %v; want %v", got, want)
	}
}

func TestAddOneNegativeOne(t *testing.T) {
	got := sample.AddOne(-1)
	want := 0
	if got != want {
		t.Errorf("AddOne(-1) = %v; want %v", got, want)
	}
}

func TestAddOneLargeNegative(t *testing.T) {
	got := sample.AddOne(-99)
	want := -98
	if got != want {
		t.Errorf("AddOne(-99) = %v; want %v", got, want)
	}
}

func TestAddOneFloatNegative(t *testing.T) {
	got := sample.AddOne(-2.25)
	want := -1.25
	if got != want {
		t.Errorf("AddOne(-2.25) = %v; want %v", got, want)
	}
}

func TestAddOneNoneRaises(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("AddOne(nil) did not panic, want TypeError")
		}
	}()
	sample.AddOne(nil)
}