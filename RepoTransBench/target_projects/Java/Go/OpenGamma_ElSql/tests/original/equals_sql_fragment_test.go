package original

import (
	"testing"
)

type MapSqlParams struct {
	data map[string]interface{}
}

func NewMapSqlParams(data map[string]interface{}) *MapSqlParams {
	return &MapSqlParams{data: data}
}

type EqualsSqlFragment struct {
	key string
}

func NewEqualsSqlFragment(key string) *EqualsSqlFragment {
	return &EqualsSqlFragment{key: key}
}

func (e *EqualsSqlFragment) ToSQL(buf *string, params *MapSqlParams) {
	val, ok := params.data[e.key[1:]] // assuming key starts with ':'
	if !ok || val == nil {
		*buf += "IS NULL "
	} else {
		*buf += "= "
	}
}

func TestEqualsSqlFragment_ValueNull(t *testing.T) {
	frag := NewEqualsSqlFragment(":foo")
	var buf string
	params := NewMapSqlParams(map[string]interface{}{})
	frag.ToSQL(&buf, params)
	if buf != "IS NULL " {
		t.Errorf("expected 'IS NULL ', got '%v'", buf)
	}
}

func TestEqualsSqlFragment_ValueNotNull(t *testing.T) {
	frag := NewEqualsSqlFragment(":foo")
	var buf string
	params := NewMapSqlParams(map[string]interface{}{"foo": 7})
	frag.ToSQL(&buf, params)
	if len(buf) < 2 || buf[:2] != "= " {
		t.Errorf("expected '= ', got '%v'", buf)
	}
}