package public_tests

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

func TestSpringSqlParams_ConstructorMapDifferentValues(t *testing.T) {
	data := map[string]interface{}{"foo": 123}
	params := NewSpringSqlParamsFromMap(data)
	if !params.Contains("foo") {
		t.Errorf("expected contains(foo) true")
	}
	if v := params.Get("foo"); v != 123 {
		t.Errorf("expected get(foo) == 123, got: %v", v)
	}
	if params.Contains("bar") {
		t.Errorf("expected contains(bar) false")
	}
	if v := params.Get("bar"); v != nil {
		t.Errorf("expected get(bar) == nil, got: %v", v)
	}
}

func TestSpringSqlParams_ConstructorNullSource(t *testing.T) {
	defer func() {
		if r := recover(); r == nil || r != "IllegalArgumentException" {
			t.Errorf("expected panic(IllegalArgumentException), got %v", r)
		}
	}()
	_ = NewSpringSqlParamsFromMap(nil)
}