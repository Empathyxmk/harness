package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func setupSingleTypeAdapter(layoutRes int) *SingleTypeAdapter[string] {
	return NewSingleTypeAdapter[string](layoutRes)
}

func TestSingleTypeAdapter_ConstructorAndGetters(t *testing.T) {
	adapter := setupSingleTypeAdapter(123)
	assert.Equal(t, 0, adapter.GetItemCount())
	assert.Equal(t, 123, adapter.GetLayoutRes())
}

func TestSingleTypeAdapter_Add(t *testing.T) {
	adapter := setupSingleTypeAdapter(321)
	adapter.Add("foo")
	assert.Equal(t, 1, adapter.GetItemCount())
}

func TestSingleTypeAdapter_AddAtPosition(t *testing.T) {
	adapter := setupSingleTypeAdapter(321)
	adapter.Add("foo")
	adapter.AddAt(0, "bar")
	assert.Equal(t, 2, adapter.GetItemCount())
}

func TestSingleTypeAdapter_SetAndAddAll(t *testing.T) {
	adapter := setupSingleTypeAdapter(321)
	adapter.Set([]string{"a", "b"})
	assert.Equal(t, 2, adapter.GetItemCount())
	adapter.AddAll([]string{"c"})
	assert.Equal(t, 3, adapter.GetItemCount())
}