package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type testMultiTypeAdapter struct {
	adapter *MultiTypeAdapter
}

func setupMultiTypeAdapter() *MultiTypeAdapter {
	adapter := NewMultiTypeAdapter()
	return adapter
}

func TestMultiTypeAdapter_AddAndViewType(t *testing.T) {
	adapter := setupMultiTypeAdapter()
	adapter.AddViewTypeToLayoutMap(1, 100)
	adapter.Add("foo", 1)
	assert.Equal(t, 1, adapter.GetItemCount())
	assert.Equal(t, 1, adapter.GetItemViewType(0))
}

func TestMultiTypeAdapter_AddAllAndSet(t *testing.T) {
	adapter := setupMultiTypeAdapter()
	adapter.AddViewTypeToLayoutMap(8, 108)

	list := []string{"a", "b"}
	adapter.AddAll(list, 8)
	assert.Equal(t, 2, adapter.GetItemCount())
	assert.Equal(t, 8, adapter.GetItemViewType(1))
	adapter.Set([]string{"x", "y"}, 8)
	assert.Equal(t, 2, adapter.GetItemCount())
	assert.Equal(t, 8, adapter.GetItemViewType(0))
}

func TestMultiTypeAdapter_RemoveClear(t *testing.T) {
	adapter := setupMultiTypeAdapter()
	adapter.AddViewTypeToLayoutMap(2, 102)
	adapter.Add("bar", 2)
	assert.Equal(t, 1, adapter.GetItemCount())
	adapter.Remove(0)
	assert.Equal(t, 0, adapter.GetItemCount())
	adapter.Add("foo", 2)
	adapter.Clear()
	assert.Equal(t, 0, adapter.GetItemCount())
}

type mockMultiViewTyper struct{}

func (m *mockMultiViewTyper) GetViewType(item interface{}) int {
	return 3
}

func TestMultiTypeAdapter_SetWithTyper(t *testing.T) {
	adapter := setupMultiTypeAdapter()
	adapter.AddViewTypeToLayoutMap(3, 103)
	adapter.SetWithTyper([]string{"f", "g"}, &mockMultiViewTyper{})
	assert.Equal(t, 2, adapter.GetItemCount())
	assert.Equal(t, 3, adapter.GetItemViewType(1))
}

func TestMultiTypeAdapter_AddAtPositionAndAddAllPosition(t *testing.T) {
	adapter := setupMultiTypeAdapter()
	adapter.AddViewTypeToLayoutMap(5, 105)

	adapter.Add("m", 5)
	adapter.AddAt(0, "n", 5)

	list := []string{"a", "b"}
	adapter.AddAllAt(0, list, 5)
	assert.Equal(t, 4, adapter.GetItemCount())
	assert.Equal(t, 5, adapter.GetItemViewType(2))
}