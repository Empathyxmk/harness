package public_tests

import (
	"testing"
)

type Package struct {
	Name string
}
type Man struct {
	Name                    string
	looksLikeAProgrammerVal bool
}
type Woman struct {
	Name                    string
	looksLikeAProgrammerVal bool
}

func (m *Man) Learn(pkg string) { m.looksLikeAProgrammerVal = true }
func (m *Man) LooksLikeAProgrammer() bool { return m.looksLikeAProgrammerVal }
func (w *Woman) Learn(pkg string) { w.looksLikeAProgrammerVal = true }
func (w *Woman) LooksLikeAProgrammer() bool { return w.looksLikeAProgrammerVal }
func NewMan(name string) *Man { return &Man{Name: name} }
func NewWoman(name string) *Woman { return &Woman{Name: name} }
func NewPackage(name string) Package { return Package{Name: name} }

func TestBecomeAProgrammerPublic(t *testing.T) {
	persons := []interface {
		Learn(pkg string)
		LooksLikeAProgrammer() bool
	}{
		NewMan("Oliver"), NewWoman("Amelia"),
		NewMan("Mason"), NewMan("Logan"), NewWoman("Harper"),
	}
	packages := []Package{NewPackage("matplotlib"), NewPackage("pandas")}
	for _, person := range persons {
		for _, pkg := range packages {
			person.Learn(pkg.Name)
			if !person.LooksLikeAProgrammer() {
				t.Errorf("Expected looksLikeAProgrammer for %v after learning %s", person, pkg.Name)
			}
		}
	}
}

func TestLearnMultiplePackagesPublic(t *testing.T) {
	persons := []interface {
		Learn(pkg string)
		LooksLikeAProgrammer() bool
	}{
		NewMan("Jack"), NewWoman("Lily"),
	}
	for _, person := range persons {
		person.Learn("sqlalchemy")
		person.Learn("httpx")
		if !person.LooksLikeAProgrammer() {
			t.Errorf("Expected looksLikeAProgrammer for %v after learning multiple packages", person)
		}
	}
}

func TestNotProgrammerInitiallyPublic(t *testing.T) {
	persons := []interface {
		Learn(pkg string)
		LooksLikeAProgrammer() bool
	}{
		NewMan("Henry"), NewWoman("Ella"),
	}
	for _, person := range persons {
		if person.LooksLikeAProgrammer() {
			t.Errorf("Did not expect to look like a programmer before learning anything")
		}
	}
}