package original

import (
	"testing"
)

type SpringSqlParams struct {
	data map[string]interface{}
}

func NewSpringSqlParamsFromMap(data map[string]interface{}) *SpringSqlParams {
	if data == nil {
		panic("IllegalArgumentException")
	}
	return &SpringSqlParams{data: data}
}

func (s *SpringSqlParams) Contains(key string) bool {
	_, ok := s.data[key]
	return ok
}

func (s *SpringSqlParams) Get(key string) interface{} {
	val, ok := s.data[key]
	if !ok {
		return nil
	}
	return val
}

func TestSpringSqlParams_ConstructorMap(t *testing.T) {
	data := map[string]interface{}{"a": "b"}
	params := NewSpringSqlParamsFromMap(data)
	if !params.Contains("a") {
		t.Errorf("expected contains(a) true")
	}
	if v := params.Get("a"); v != "b" {
		t.Errorf("expected get(a) == 'b', got: %v", v)
	}
	if params.Contains("x") {
		t.Errorf("expected contains(x) false")
	}
	if v := params.Get("x"); v != nil {
		t.Errorf("expected get(x) == nil, got: %v", v)
	}
}

func TestSpringSqlParams_ConstructorNull(t *testing.T) {
	defer func() {
		if r := recover(); r == nil || r != "IllegalArgumentException" {
			t.Errorf("expected panic(IllegalArgumentException), got %v", r)
		}
	}()
	_ = NewSpringSqlParamsFromMap(nil)
}