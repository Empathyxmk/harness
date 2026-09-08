package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type mockMultiViewTyperPublic struct{}

func (m *mockMultiViewTyperPublic) GetViewType(item interface{}) int {
	return 4
}

func TestMultiTypeAdapterPublic_AddAndViewTypePublic(t *testing.T) {
	adapter := NewMultiTypeAdapter()
	adapter.AddViewTypeToLayoutMap(9, 109)
	adapter.Add("baz", 9)
	assert.Equal(t, 1, adapter.GetItemCount())
	assert.Equal(t, 9, adapter.GetItemViewType(0))
}

func TestMultiTypeAdapterPublic_AddAllAndSetPublic(t *testing.T) {
	adapter := NewMultiTypeAdapter()
	adapter.AddViewTypeToLayoutMap(11, 111)

	list := []string{"p", "q", "r"}
	adapter.AddAll(list, 11)
	assert.Equal(t, 3, adapter.GetItemCount())
	assert.Equal(t, 11, adapter.GetItemViewType(2))
	adapter.Set([]string{"v", "w", "z"}, 11)
	assert.Equal(t, 3, adapter.GetItemCount())
	assert.Equal(t, 11, adapter.GetItemViewType(0))
}

func TestMultiTypeAdapterPublic_RemoveClearPublic(t *testing.T) {
	adapter := NewMultiTypeAdapter()
	adapter.AddViewTypeToLayoutMap(7, 107)
	adapter.Add("car", 7)
	assert.Equal(t, 1, adapter.GetItemCount())
	adapter.Remove(0)
	assert.Equal(t, 0, adapter.GetItemCount())
	adapter.Add("bus", 7)
	adapter.Clear()
	assert.Equal(t, 0, adapter.GetItemCount())
}

func TestMultiTypeAdapterPublic_SetWithTyperPublic(t *testing.T) {
	adapter := NewMultiTypeAdapter()
	adapter.AddViewTypeToLayoutMap(4, 104)
	adapter.SetWithTyper([]string{"k", "l", "m"}, &mockMultiViewTyperPublic{})
	assert.Equal(t, 3, adapter.GetItemCount())
	assert.Equal(t, 4, adapter.GetItemViewType(2))
}

func TestMultiTypeAdapterPublic_AddAtPositionAndAddAllPositionPublic(t *testing.T) {
	adapter := NewMultiTypeAdapter()
	adapter.AddViewTypeToLayoutMap(15, 115)

	adapter.Add("apple", 15)
	adapter.AddAt(0, "banana", 15)

	list := []string{"pear", "peach"}
	adapter.AddAllAt(0, list, 15)
	assert.Equal(t, 4, adapter.GetItemCount())
	assert.Equal(t, 15, adapter.GetItemViewType(3))
}