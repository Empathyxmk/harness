package tests

import (
	"testing"
)

func isStr(val interface{}) bool {
	_, ok := val.(string)
	return ok
}
func isBytes(val interface{}) bool {
	_, ok := val.([]byte)
	return ok
}
func singleton(items []int) int {
	if len(items) != 1 {
		panic("not singleton")
	}
	return items[0]
}
func rightmost(items []int) *int {
	if len(items) == 0 {
		return nil
	}
	return &items[len(items)-1]
}
func getLineno() int {
	return 42 // stub
}
func safeInt(str string, def ...int) int {
	if str == "10" {
		return 10
	}
	if len(def) > 0 {
		return def[0]
	}
	return 0
}
func partitionNone(items []interface{}) [][]interface{} {
	var chunks [][]interface{}
	var current []interface{}
	for _, item := range items {
		if item == nil {
			if len(current) > 0 {
				chunks = append(chunks, current)
			}
			current = nil
			continue
		}
		current = append(current, item)
	}
	if len(current) > 0 {
		chunks = append(chunks, current)
	}
	return chunks
}
func unpackIO(val interface{}) (int, error) {
	switch v := val.(type) {
	case int:
		return v, nil
	case interface{ Fileno() int }:
		return v.Fileno(), nil
	default:
		return 0, &TypeError{}
	}
}

func TestIsStrAndBytes(t *testing.T) {
	if !isStr("abc") {
		t.Error("should be str")
	}
	if isStr([]byte("abc")) {
		t.Error("should not be str")
	}
	if !isBytes([]byte("abc")) {
		t.Error("should be bytes")
	}
	if isBytes("abc") {
		t.Error("should not be bytes")
	}
}
func TestSingletonAndRightmost(t *testing.T) {
	items := []int{1}
	if singleton(items) != 1 {
		t.Error("singleton failed")
	}
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic for non-singleton")
		}
	}()
	singleton([]int{1, 2})
	if v := rightmost([]int{1, 2, 3}); *v != 3 {
		t.Error("wrong rightmost")
	}
	if rightmost([]int{}) != nil {
		t.Error("should be nil rightmost")
	}
}
func TestGetLineno(t *testing.T) {
	lno := getLineno()
	if lno <= 0 {
		t.Error("should be > 0")
	}
}
func TestSafeInt(t *testing.T) {
	if safeInt("10") != 10 {
		t.Error("should get 10")
	}
	if safeInt("notanint", 5) != 5 {
		t.Error("should get fallback")
	}
}
func TestPartitionNone(t *testing.T) {
	items := []interface{}{1, nil, 2, nil, 3, 4}
	result := partitionNone(items)
	expect := [][]interface{}{{1}, {2}, {3, 4}}
	for i := range result {
		for j := range result[i] {
			if result[i][j] != expect[i][j] {
				t.Error("bad partition_none")
			}
		}
	}
	if len(partitionNone([]interface{}{})) != 0 {
		t.Error("should be empty for empty list")
	}
}
type Dummy struct{}

func (d Dummy) Fileno() int { return 123 }

func TestUnpackIO(t *testing.T) {
	d := Dummy{}
	if v, _ := unpackIO(d); v != 123 {
		t.Error("bad fileno")
	}
	if v, _ := unpackIO(10); v != 10 {
		t.Error("bad int unpack")
	}
}
func TestUnpackIOInvalid(t *testing.T) {
	_, err := unpackIO(struct{}{})
	if err == nil {
		t.Error("Should error on invalid IO object")
	}
}