package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

func TestDumpDefaultDict(t *testing.T) {
	d := map[string]string{
		"a": "A",
		"b": "B",
	}
	dd := jsons.NewDefaultDictStringList(d)
	dumped := jsons.Dump(dd)
	assert.Equal(t, d, dumped)
}

func TestLoadDefaultDict(t *testing.T) {
	d := map[string][]int{"a": {1, 2, 3}}
	dd := jsons.NewDefaultDictIntList(d)
	loaded := jsons.LoadDefaultDictStringList(d)
	assert.Equal(t, dd, loaded)
	assert.True(t, jsons.IsDefaultDict(loaded))
	assert.Equal(t, "[]int", jsons.DefaultFactoryType(loaded))
}

func TestLoadDefaultDictWithoutArgs(t *testing.T) {
	d := map[string][]int{"a": {1, 2, 3}}
	dd := jsons.NewDefaultDictRaw(d)
	loaded := jsons.LoadDefaultDictRaw(d)
	assert.Equal(t, dd, loaded)
	assert.Equal(t, jsons.DefaultFactoryType(dd), jsons.DefaultFactoryType(loaded))
}