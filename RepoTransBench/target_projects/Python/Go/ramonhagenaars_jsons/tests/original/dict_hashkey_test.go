package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

type Foo struct{ A, B, C int }
type DFoo struct{ A, B int }

func (d DFoo) Equal(other DFoo) bool { return d.A == other.A && d.B == other.B }

func TestDictHashKeyWithSerializer(t *testing.T) {
	fooSerializer := func(obj Foo) string {
		return string(rune(obj.A + '0')) + "," + string(rune(obj.B+'0')) + "," + string(rune(obj.C+'0'))
	}
	fooDeserializer := func(s string) Foo {
		// Decode e.g. "1,2,3"
		return Foo{A: int(s[0] - '0'), B: int(s[2] - '0'), C: int(s[4] - '0')}
	}
	jsons.SetFooSerializer(fooSerializer)
	jsons.SetFooDeserializer(fooDeserializer)
	bar := map[Foo]DFoo{Foo{1, 2, 3}: DFoo{42, 39}}
	dumped := jsons.DumpBarWithOptions(bar)
	assert.Equal(t, map[string]interface{}{"1,2,3": map[string]int{"A": 42, "B": 39}}, dumped)
	loaded := jsons.LoadBarWithOptions(dumped)
	assert.Equal(t, bar, loaded)
}

func TestDictHashKey(t *testing.T) {
	bar := map[Foo]DFoo{Foo{1, 2, 3}: DFoo{42, 39}}
	dumped := jsons.DumpBarWithOptions(bar)
	loaded := jsons.LoadBarWithOptions(dumped)
	assert.Equal(t, bar, loaded)
}