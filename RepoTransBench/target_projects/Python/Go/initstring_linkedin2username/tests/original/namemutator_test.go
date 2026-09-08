package original

import (
	"testing"
	"reflect"

	"github.com/example/initstring_linkedin2username"
)

// This table reflects the tested inputs/expected outputs.
func TestCleanAndSplitName(t *testing.T) {
	cases := []struct {
		Input    string
		Expected map[string]string
	}{
		{"John Smith", map[string]string{"first": "john", "last": "smith", "second": ""}},
		{"Jane D'oe", map[string]string{"first": "jane", "last": "doe", "second": ""}},
		{"Dr. Ángela Gómez (MBA, PhD)", map[string]string{"first": "angela", "last": "gomez", "second": ""}},
		{"José Niño", map[string]string{"first": "jose", "last": "nino", "second": ""}},
		{"Joe (CTO) Bloggs", map[string]string{"first": "joe", "last": "bloggs", "second": ""}},
	}
	for _, c := range cases {
		nm := linkedin2username.NewNameMutator(c.Input)
		if !reflect.DeepEqual(nm.Name(), c.Expected) {
			t.Errorf("input=%q, got=%#v, want=%#v", c.Input, nm.Name(), c.Expected)
		}
	}
}