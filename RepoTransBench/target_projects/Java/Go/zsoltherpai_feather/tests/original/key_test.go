package original

import (
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
)

type Q1 struct{}

type Key struct {
	typ       reflect.Type
	qualifier interface{}
	name      string
}

func KeyOf(typ reflect.Type, qualifierOrName ...interface{}) *Key {
	k := &Key{typ: typ}
	if len(qualifierOrName) == 1 {
		switch v := qualifierOrName[0].(type) {
		case reflect.Type:
			k.qualifier = v
		case string:
			k.qualifier = reflect.TypeOf("") // Named
			k.name = v
		}
	} else if len(qualifierOrName) == 2 {
		k.qualifier = qualifierOrName[1]
	}
	return k
}

func (k *Key) Equal(other *Key) bool {
	return k.typ == other.typ &&
		reflect.DeepEqual(k.qualifier, other.qualifier) &&
		k.name == other.name
}

func (k *Key) HashCode() int {
	// Not meaningful in Go, but let's simulate a hash
	return int(k.typ.Size()) + len(k.name)
}

func (k *Key) String() string {
	if k.name != "" {
		return k.typ.String() + "@\"" + k.name + "\""
	} else if k.qualifier != nil {
		switch qual := k.qualifier.(type) {
		case reflect.Type:
			return k.typ.String() + "@" + qual.Name()
		default:
			return k.typ.String() + "@unknown"
		}
	}
	return k.typ.String()
}

func TestKeyEqualitySameType(t *testing.T) {
	k1 := KeyOf(reflect.TypeOf(""))
	k2 := KeyOf(reflect.TypeOf(""))
	assert.True(t, k1.Equal(k2))
	assert.Equal(t, k1.HashCode(), k2.HashCode())
}

func TestKeyInequalityType(t *testing.T) {
	k1 := KeyOf(reflect.TypeOf(""))
	k2 := KeyOf(reflect.TypeOf(0))
	assert.False(t, k1.Equal(k2))
}

func TestKeyWithQualifierAnnotation(t *testing.T) {
	k1 := KeyOf(reflect.TypeOf(""), reflect.TypeOf(Q1{}))
	assert.Equal(t, reflect.TypeOf(Q1{}), k1.qualifier)
	assert.Empty(t, k1.name)
	assert.Equal(t, "string@Q1", k1.String())
}

func TestKeyWithNamed(t *testing.T) {
	k1 := KeyOf(reflect.TypeOf(""), "name")
	// Named is simulated with string type
	assert.Equal(t, reflect.TypeOf(""), k1.qualifier)
	assert.Equal(t, "name", k1.name)
	assert.Equal(t, "string@\"name\"", k1.String())
}

func TestKeyWithQualifierObject(t *testing.T) {
	q1 := Q1{}
	k := KeyOf(reflect.TypeOf(""), reflect.TypeOf(Q1{}))
	assert.Equal(t, reflect.TypeOf(Q1{}), k.qualifier)
	assert.Empty(t, k.name)
}

func TestKeyWithNamedQualifierObject(t *testing.T) {
	k := KeyOf(reflect.TypeOf(""), "foo")
	assert.Equal(t, reflect.TypeOf(""), k.qualifier)
	assert.Equal(t, "foo", k.name)
}

func TestEqualsAndHashCodeNullQualifierName(t *testing.T) {
	k1 := KeyOf(reflect.TypeOf(""))
	k2 := KeyOf(reflect.TypeOf(""))
	assert.True(t, k1.Equal(k2))
	assert.Equal(t, k1.HashCode(), k2.HashCode())
}

func TestNotEqualsIfQualifierDiffers(t *testing.T) {
	k1 := KeyOf(reflect.TypeOf(""))
	k2 := KeyOf(reflect.TypeOf(""), reflect.TypeOf(Q1{}))
	assert.False(t, k1.Equal(k2))
}

func TestNotEqualsIfNameDiffers(t *testing.T) {
	k1 := KeyOf(reflect.TypeOf(""), "name1")
	k2 := KeyOf(reflect.TypeOf(""), "name2")
	assert.False(t, k1.Equal(k2))
}