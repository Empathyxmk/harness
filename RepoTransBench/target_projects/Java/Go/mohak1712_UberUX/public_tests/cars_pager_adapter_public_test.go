package public_tests

import (
	"testing"
	"mohak1712_uberux/tests"
	"github.com/stretchr/testify/assert"
)

func TestCarsPagerAdapterGetCountReturnsListSizePublic(t *testing.T) {
	adapter := tests.NewCarsPagerAdapter([]int{2, 3, 2})
	assert.Equal(t, 3, adapter.GetCount())
}

func TestCarsPagerAdapterIsViewFromObjectReturnsTrueIfSamePublic(t *testing.T) {
	adapter := tests.NewCarsPagerAdapter([]int{2, 3, 2})
	view := struct{}{}
	assert.True(t, adapter.IsViewFromObject(view, view))
}

func TestCarsPagerAdapterInstantiateAndDestroyItemNoCrashPublic(t *testing.T) {
	adapter := tests.NewCarsPagerAdapter([]int{2, 3, 2})
	container := struct{}{}
	adapter.InstantiateItem(container, 1)
	adapter.DestroyItem(container, 2, struct{}{})
}