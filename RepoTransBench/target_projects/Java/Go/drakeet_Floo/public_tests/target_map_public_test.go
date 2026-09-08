package public_tests

import "testing"

type TargetMap struct {
	data map[string]string
}
func NewTargetMap() *TargetMap {
	return &TargetMap{data: map[string]string{}}
}

func (m *TargetMap) Put(k, v string) {
	m.data[k] = v
}
func (m *TargetMap) Get(k string) *string {
	val, ok := m.data[k]
	if !ok {
		return nil
	}
	return &val
}

func TestPutAndGet_public(t *testing.T) {
	m := NewTargetMap()
	m.Put("/my/path", "targetValue")
	got := m.Get("/my/path")
	if got == nil || *got != "targetValue" {
		t.Errorf("expected 'targetValue', got %v", got)
	}
}

func TestGetNonExistingKey_public(t *testing.T) {
	m := NewTargetMap()
	got := m.Get("/no/such/key")
	if got != nil {
		t.Error("expected nil for non existing key")
	}
}