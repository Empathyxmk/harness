package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type dummyDataBindingPublic struct {
	Root any
}

func (d *dummyDataBindingPublic) GetRoot() any {
	return d.Root
}

func TestBindingViewHolderPublic_GetBindingPublic(t *testing.T) {
	binding := &dummyDataBindingPublic{Root: "view"}
	holder := NewBindingViewHolder(binding)
	assert.Equal(t, binding, holder.GetBinding())
}