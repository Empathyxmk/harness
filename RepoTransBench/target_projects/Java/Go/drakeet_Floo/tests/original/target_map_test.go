package original

import "testing"

type Target struct {
	Route      string
	TargetClass string
}
type TargetMap struct {
	data map[string]*Target
}
func NewTargetMap() *TargetMap {
	return &TargetMap{data: map[string]*Target{}}
}
func (m *TargetMap) Put(key string, t *Target) {
	m.data[key] = t
}
func (m *TargetMap) Get(key string) *Target {
	return m.data[key]
}
func (m *TargetMap) Remove(key string) {
	delete(m.data, key)
}
func (m *TargetMap) ContainsKey(key string) bool {
	_, ok := m.data[key]
	return ok
}
func (m *TargetMap) IsEmpty() bool {
	return len(m.data) == 0
}

func TestPutAndGet(t *testing.T) {
	m := NewTargetMap()
	t1 := &Target{"route1", "activity1"}
	m.Put("key", t1)
	if !m.ContainsKey("key") {
		t.Error("Map should contain key")
	}
	if got := m.Get("key"); got != t1 {
		t.Errorf("Map did not return expected Target, got: %#v", got)
	}
}

func TestRemove(t *testing.T) {
	m := NewTargetMap()
	t1 := &Target{"route2", "activity2"}
	m.Put("rm", t1)
	m.Remove("rm")
	if m.ContainsKey("rm") {
		t.Error("Map still contains removed key")
	}
}

func TestIsEmpty_Map(t *testing.T) {
	m := NewTargetMap()
	if !m.IsEmpty() {
		t.Error("Map should be empty initially")
	}
	m.Put("a", &Target{"a", "a"})
	m.Remove("a")
	if !m.IsEmpty() {
		t.Error("Map should be empty after put-remove")
	}
}