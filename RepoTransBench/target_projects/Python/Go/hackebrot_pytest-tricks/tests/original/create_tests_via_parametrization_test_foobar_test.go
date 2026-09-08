package original

import (
	"testing"
)

type Package struct {
	Name         string
	License      string
	IsOpenSource bool
}

func NewPackage(name, license string) Package {
	isOpenSource := false
	switch license {
	case "Apache 2.0", "BSD", "MIT":
		isOpenSource = true
	}
	return Package{
		Name:         name,
		License:      license,
		IsOpenSource: isOpenSource,
	}
}

type Person interface {
	Learn(pkg string)
	LooksLikeAProgrammer() bool
}

type Woman struct {
	Name                    string
	programmingLanguages    map[string]bool
	looksLikeAProgrammerVal bool
}

func NewWoman(name string) *Woman {
	return &Woman{
		Name:                 name,
		programmingLanguages: make(map[string]bool),
	}
}

func (w *Woman) Learn(pkg string) {
	w.programmingLanguages[pkg] = true
	w.looksLikeAProgrammerVal = true
}

func (w *Woman) LooksLikeAProgrammer() bool {
	return w.looksLikeAProgrammerVal
}

type Man struct {
	Name                    string
	programmingLanguages    map[string]bool
	looksLikeAProgrammerVal bool
}

func NewMan(name string) *Man {
	return &Man{
		Name:                 name,
		programmingLanguages: make(map[string]bool),
	}
}

func (m *Man) Learn(pkg string) {
	m.programmingLanguages[pkg] = true
	m.looksLikeAProgrammerVal = true
}

func (m *Man) LooksLikeAProgrammer() bool {
	return m.looksLikeAProgrammerVal
}

var packages = []Package{
	NewPackage("requests", "Apache 2.0"),
	NewPackage("django", "BSD"),
	NewPackage("pytest", "MIT"),
}

func TestBecomeAProgrammer(t *testing.T) {
	persons := []Person{
		NewWoman("Audrey"), NewWoman("Brianna"),
		NewMan("Daniel"), NewWoman("Ola"), NewMan("Kenneth"),
	}
	for _, pkg := range packages {
		for _, person := range persons {
			person.Learn(pkg.Name)
			if !person.LooksLikeAProgrammer() {
				t.Errorf("Expected %v to look like a programmer after learning %v", person, pkg.Name)
			}
		}
	}
}

func TestIsOpenSource(t *testing.T) {
	for _, pkg := range packages {
		if !pkg.IsOpenSource {
			t.Errorf("Expected package %v to be open source", pkg.Name)
		}
	}
}