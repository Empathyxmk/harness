package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type dummyDataBinding struct {
	Root any
}

func (d *dummyDataBinding) GetRoot() any {
	return d.Root
}

func TestBindingViewHolder_GetBinding(t *testing.T) {
	binding := &dummyDataBinding{Root: "view"}
	holder := NewBindingViewHolder(binding)
	assert.Equal(t, binding, holder.GetBinding())
}