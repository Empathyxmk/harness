package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type testBaseViewAdapter struct {
	*BaseViewAdapter[string]
}

func newTestBaseViewAdapter() *testBaseViewAdapter {
	adapter := &testBaseViewAdapter{
		BaseViewAdapter: NewBaseViewAdapter[string](),
	}
	adapter.mCollection = []string{"a", "b", "c"}
	return adapter
}

func TestBaseViewAdapter_Remove(t *testing.T) {
	adapter := newTestBaseViewAdapter()
	adapter.Remove(1)
	assert.Equal(t, 2, adapter.GetItemCount())
	assert.Equal(t, "a", adapter.mCollection[0])
	assert.Equal(t, "c", adapter.mCollection[1])
}

func TestBaseViewAdapter_Clear(t *testing.T) {
	adapter := newTestBaseViewAdapter()
	adapter.Clear()
	assert.Equal(t, 0, adapter.GetItemCount())
}

type dummyPresenter struct{}
type dummyDecorator struct{}

func TestBaseViewAdapter_SetPresenterAndDecorator(t *testing.T) {
	adapter := newTestBaseViewAdapter()
	p := &dummyPresenter{}
	adapter.SetPresenter(p)
	assert.Equal(t, p, adapter.GetPresenter())

	d := &dummyDecorator{}
	adapter.SetDecorator(d)
	assert.NotNil(t, adapter.mDecorator)
}