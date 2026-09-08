package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSingleTypeAdapterPublic_AddAndCountPublic(t *testing.T) {
	adapter := NewSingleTypeAdapter[string](1222)
	adapter.Add("delta")
	assert.Equal(t, 1, adapter.GetItemCount())
	assert.Equal(t, 1222, adapter.GetLayoutRes())
}

func TestSingleTypeAdapterPublic_AddAtPositionPublic(t *testing.T) {
	adapter := NewSingleTypeAdapter[string](2121)
	adapter.Add("sigma")
	adapter.AddAt(0, "theta")
	assert.Equal(t, 2, adapter.GetItemCount())
	assert.Equal(t, "theta", adapter.mCollection[0])
	assert.Equal(t, "sigma", adapter.mCollection[1])
}

func TestSingleTypeAdapterPublic_SetPublic(t *testing.T) {
	adapter := NewSingleTypeAdapter[string](3333)
	items := []string{"alpha", "beta", "gamma"}
	adapter.Set(items)
	assert.Equal(t, 3, adapter.GetItemCount())
	assert.Equal(t, "alpha", adapter.mCollection[0])
	assert.Equal(t, "gamma", adapter.mCollection[2])
}

func TestSingleTypeAdapterPublic_AddAllPublic(t *testing.T) {
	adapter := NewSingleTypeAdapter[string](4343)
	items := []string{"one", "two"}
	adapter.AddAll(items)
	assert.Equal(t, 2, adapter.GetItemCount())
	adapter.Add("three")
	assert.Equal(t, 3, adapter.GetItemCount())
}