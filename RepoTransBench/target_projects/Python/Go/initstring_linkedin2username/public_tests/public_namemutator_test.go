package public_tests

import (
	"reflect"
	"testing"

	"github.com/example/initstring_linkedin2username"
)

func TestCleanAndSplitNamePublic(t *testing.T) {
	cases := []struct {
		Input    string
		Expected map[string]string
	}{
		{"Sam Lee", map[string]string{"first": "sam", "last": "lee", "second": ""}},
		{"Ms. Eva O'Brien", map[string]string{"first": "eva", "last": "obrien", "second": ""}},
		{"Prof. Łukasz Nowak (PhD)", map[string]string{"first": "lukasz", "last": "nowak", "second": ""}},
		{"María-José Carreño", map[string]string{"first": "maria", "last": "carreno", "second": ""}},
		{"Chris (CEO) Smithers", map[string]string{"first": "chris", "last": "smithers", "second": ""}},
	}
	for _, c := range cases {
		nm := linkedin2username.NewNameMutator(c.Input)
		if !reflect.DeepEqual(nm.Name(), c.Expected) {
			t.Errorf("input=%q, got=%#v, want=%#v", c.Input, nm.Name(), c.Expected)
		}
	}
}