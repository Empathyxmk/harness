// Code generated from src/latexify/config_test.py
package original

import (
	"testing"
	"github.com/yourusername/googlelatexify/latexify/config"
)

func TestMergeFieldPrecedenceAndTypes(t *testing.T) {
	conf := config.Defaults().Merge(config.Opt{
		ExpandFunctions: map[string]struct{}{"f": {}},
		Identifiers: map[string]string{"a": "b"},
		Prefixes: map[string]struct{}{"p.":{}},
		ReduceAssignments: true,
		UseMathSymbols: true,
		UseSetSymbols: true,
		UseSignature: false,
		EscapeUnderscores: false,
	})
	merged := conf.Merge(config.Opt{ExpandFunctions: nil})
	if !setEqual(merged.ExpandFunctions, map[string]struct{}{"f": {}}) {
		t.Errorf("ExpandFunctions not retained: %v", merged.ExpandFunctions)
	}
}

func TestStrAndRepr(t *testing.T) {
	conf := config.Defaults()
	s := conf.String()
	r := conf.String() // assuming String = repr in Go
	if !(contains(s, "expand_functions") && contains(r, "expand_functions")) {
		t.Errorf("Expected expand_functions in config string and repr, got s=%v r=%v", s, r)
	}
}

func TestDefaultsIsAConfig(t *testing.T) {
	conf := config.Defaults()
	if conf == nil {
		t.Fatal("Defaults returned nil Config")
	}
}

func TestMergeDifferentTypes(t *testing.T) {
	c1 := config.Defaults()
	c2 := c1.Merge(config.Opt{UseMathSymbols: false})
	if c2.UseMathSymbols != false {
		t.Error("Expected UseMathSymbols=false")
	}
}

// Helper function for set comparison
func setEqual(a, b map[string]struct{}) bool {
	if len(a) != len(b) {
		return false
	}
	for key := range a {
		if _, ok := b[key]; !ok {
			return false
		}
	}
	return true
}

func contains(str, sub string) bool {
	return len(str) >= len(sub) && (str == sub || (len(str) > len(sub) && (str[:len(sub)] == sub || contains(str[1:], sub))))
}