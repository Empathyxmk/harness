package public_tests

import (
	"reflect"
	"testing"

	"github.com/example/initstring_linkedin2username"
)

func TestPublicFLast(t *testing.T) {
	out := linkedin2username.FLast("Nina", "Simone")
	if out != "nsimone" {
		t.Errorf("expected nsimone, got %v", out)
	}
}

func TestPublicFDotLast(t *testing.T) {
	out := linkedin2username.FDotLast("Albert", "King")
	if out != "a.king" {
		t.Errorf("expected a.king, got %v", out)
	}
}

func TestPublicLastF(t *testing.T) {
	out := linkedin2username.LastF("Armstrong", "Louis")
	if out != "armstrongl" {
		t.Errorf("expected armstrongl, got %v", out)
	}
}

func TestPublicFirstDotLast(t *testing.T) {
	out := linkedin2username.FirstDotLast("Bessie", "Smith")
	if out != "bessie.smith" {
		t.Errorf("expected bessie.smith, got %v", out)
	}
}

func TestPublicFirstL(t *testing.T) {
	out := linkedin2username.FirstL("Duke", "Ellington")
	if out != "dukee" {
		t.Errorf("expected duke, got %v", out)
	}
}

func TestPublicFirst(t *testing.T) {
	out := linkedin2username.FirstOnly("Ella", "Fitzgerald")
	if out != "ella" {
		t.Errorf("expected ella, got %v", out)
	}
}

func TestPublicCleanName(t *testing.T) {
	if linkedin2username.CleanName(" Ray   Charles Jr.") != "ray charles jr" {
		t.Errorf("failed to clean name Ray Charles Jr")
	}
	if linkedin2username.CleanName("Dinah (CEO) Washington") != "dinah washington" {
		t.Errorf("failed to clean name Dinah Washington")
	}
	if linkedin2username.CleanName("Count Basie.") != "count basie" {
		t.Errorf("failed to clean name Count Basie")
	}
}

func TestPublicSplitName(t *testing.T) {
	first, last, second := linkedin2username.SplitName("Ruth Brown")
	if first != "ruth" || last != "brown" || second != "" {
		t.Errorf("Ruth Brown split: got %q %q %q", first, last, second)
	}
	first, last, second = linkedin2username.SplitName("Roy Orbison (VP)")
	if first != "roy" || last != "orbison" || second != "" {
		t.Errorf("Roy Orbison split: got %q %q %q", first, last, second)
	}
	first, last, second = linkedin2username.SplitName("Mr. Charles")
	if first != "charles" || last != "" || second != "" {
		t.Errorf("Mr. Charles split: got %q %q %q", first, last, second)
	}
}

func TestPublicFindEmployees(t *testing.T) {
	type employee struct {
		Name string `json:"name"`
	}
	employees := []employee{
		{"Oscar Peterson"},
		{"Sarah Vaughan"},
		{"Mahalia Jackson"},
	}
	// The function in Go should accept []employee, return same (as a stub).
	found := linkedin2username.FindEmployeesPublicDummy(employees)
	if !reflect.DeepEqual(employees, found) {
		t.Errorf("FindEmployees did not return all employees")
	}
}