package original

import (
	"testing"
	"pypa_sampleproject/src/sample"
)

func TestAddOnePositive(t *testing.T) {
	got := sample.AddOne(2)
	want := 3
	if got != want {
		t.Errorf("AddOne(2) = %v; want %v", got, want)
	}
}

func TestAddOneZero(t *testing.T) {
	got := sample.AddOne(0)
	want := 1
	if got != want {
		t.Errorf("AddOne(0) = %v; want %v", got, want)
	}
}

func TestAddOneNegative(t *testing.T) {
	got := sample.AddOne(-5)
	want := -4
	if got != want {
		t.Errorf("AddOne(-5) = %v; want %v", got, want)
	}
}

func TestAddOneFloat(t *testing.T) {
	got := sample.AddOne(2.5)
	want := 3.5
	if got != want {
		t.Errorf("AddOne(2.5) = %v; want %v", got, want)
	}
}

func TestAddOneStrRaises(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("AddOne(\"hi\") did not panic, want TypeError")
		}
	}()
	sample.AddOne("hi")
}