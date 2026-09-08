package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type testBaseViewAdapterPublic struct {
	*BaseViewAdapter[string]
}

func newTestBaseViewAdapterPublic() *testBaseViewAdapterPublic {
	adapter := &testBaseViewAdapterPublic{
		BaseViewAdapter: NewBaseViewAdapter[string](),
	}
	return adapter
}

func TestBaseViewAdapterPublic_AddSetClearPublic(t *testing.T) {
	adapter := newTestBaseViewAdapterPublic()
	adapter.Add("red")
	assert.Equal(t, 1, adapter.GetItemCount())
	adapter.Set([]string{"yellow", "green", "blue"})
	assert.Equal(t, 3, adapter.GetItemCount())
	adapter.Clear()
	assert.Equal(t, 0, adapter.GetItemCount())
}

func TestBaseViewAdapterPublic_RemoveGetPublic(t *testing.T) {
	adapter := newTestBaseViewAdapterPublic()
	adapter.Set([]string{"x", "y", "z"})
	assert.Equal(t, "y", adapter.Get(1))
	adapter.Remove(0)
	assert.Equal(t, "y", adapter.Get(0))
	assert.Equal(t, 2, adapter.GetItemCount())
}