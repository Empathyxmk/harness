package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

func TestDumpOrderedDict(t *testing.T) {
	d := map[string]string{"a": "A", "b": "B"}
	od := jsons.NewOrderedDict(d)
	dumped := jsons.Dump(od)
	assert.Equal(t, d, dumped)
}

func TestLoadOrderedDict(t *testing.T) {
	d := map[string]string{"a": "A", "b": "B"}
	var loaded map[string]string
	jsons.Load(d, &loaded)
	assert.Equal(t, d, loaded)
}