package original

import (
	"testing"

	"mohak1712_uberux/tests"
	"github.com/stretchr/testify/assert"
)

func TestCarsPagerAdapterGetCountReturnsListSize(t *testing.T) {
	adapter := tests.NewCarsPagerAdapter([]int{0, 1})
	assert.Equal(t, 2, adapter.GetCount())
}

func TestCarsPagerAdapterIsViewFromObjectReturnsTrueIfSame(t *testing.T) {
	adapter := tests.NewCarsPagerAdapter([]int{0, 1})
	view := struct{}{}
	assert.True(t, adapter.IsViewFromObject(view, view))
}

func TestCarsPagerAdapterInstantiateAndDestroyItemNoCrash(t *testing.T) {
	adapter := tests.NewCarsPagerAdapter([]int{0, 1})
	container := struct{}{} // simple stand-in for ViewGroup
	adapter.InstantiateItem(container, 0)
	adapter.DestroyItem(container, 0, struct{}{})
}