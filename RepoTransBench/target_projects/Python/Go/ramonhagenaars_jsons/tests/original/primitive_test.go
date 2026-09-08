package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

func TestDumpStr(t *testing.T) {
	assert.Equal(t, "some string", jsons.Dump("some string"))
}

func TestDumpInt(t *testing.T) {
	assert.Equal(t, 123, jsons.Dump(123))
}

func TestDumpFloat(t *testing.T) {
	assert.Equal(t, 123.456, jsons.Dump(123.456))
}

func TestDumpBool(t *testing.T) {
	assert.Equal(t, true, jsons.Dump(true))
}

func TestDumpNone(t *testing.T) {
	assert.Equal(t, nil, jsons.Dump(nil))
}

func TestDumpAndCast(t *testing.T) {
	assert.Equal(t, 42, jsons.Dump("42", "int"))
	assert.Equal(t, 42.0, jsons.Dump("42", "float"))
	assert.Equal(t, "42", jsons.Dump(42, "string"))
	assert.Equal(t, true, jsons.Dump(42, "bool"))
	_, err := jsons.Dump("fortytwo", "int")
	assert.Error(t, err)
}

func TestLoadStr(t *testing.T) {
	assert.Equal(t, "some string", jsons.Load("some string"))
}

func TestLoadInt(t *testing.T) {
	assert.Equal(t, 123, jsons.Load(123))
}

func TestLoadFloat(t *testing.T) {
	assert.Equal(t, 123.456, jsons.Load(123.456))
}

func TestLoadBool(t *testing.T) {
	assert.Equal(t, true, jsons.Load(true))
}

func TestLoadAndCast(t *testing.T) {
	assert.Equal(t, 42, jsons.Load("42", "int"))
	assert.Equal(t, 42.0, jsons.Load("42", "float"))
	assert.Equal(t, "42", jsons.Load(42, "string"))
	assert.Equal(t, true, jsons.Load(42, "bool"))
	_, err := jsons.Load("fortytwo", "int")
	assert.Error(t, err)
}