package original

import (
	"testing"
)

// DummyAdapter mimics a ListAdapter with integer data.
type DummyAdapter struct {
	data []int
}

func NewDummyAdapter(data []int) *DummyAdapter {
	return &DummyAdapter{data: data}
}

func (a *DummyAdapter) Get(index int) int {
	return a.data[index]
}
func (a *DummyAdapter) Size() int {
	return len(a.data)
}
func (a *DummyAdapter) AreAllItemsEnabled() bool {
	return true
}
func (a *DummyAdapter) IsEnabled(position int) bool {
	return true
}
func (a *DummyAdapter) GetCount() int {
	return len(a.data)
}
func (a *DummyAdapter) GetItem(position int) int {
	return a.data[position]
}
func (a *DummyAdapter) GetItemId(position int) int64 {
	return int64(position)
}
func (a *DummyAdapter) HasStableIds() bool {
	return false
}
func (a *DummyAdapter) GetItemViewType(position int) int {
	return 0
}
func (a *DummyAdapter) GetViewTypeCount() int {
	return 1
}
func (a *DummyAdapter) IsEmpty() bool {
	return len(a.data) == 0
}

// MergeAdapter is a minimal composite adapter, combining DummyAdapter instances.
type MergeAdapter struct {
	adapters []*DummyAdapter
}

func NewMergeAdapter(adapters ...*DummyAdapter) *MergeAdapter {
	list := []*DummyAdapter{}
	for _, a := range adapters {
		list = append(list, a)
	}
	return &MergeAdapter{adapters: list}
}

func (ma *MergeAdapter) AddAdapter(adapter *DummyAdapter) {
	ma.adapters = append(ma.adapters, adapter)
}

func (ma *MergeAdapter) GetCount() int {
	count := 0
	for _, a := range ma.adapters {
		count += a.GetCount()
	}
	return count
}

func (ma *MergeAdapter) GetItem(pos int) int {
	offset := 0
	for _, a := range ma.adapters {
		if pos < offset+a.GetCount() {
			return a.GetItem(pos - offset)
		}
		offset += a.GetCount()
	}
	panic("index out of range in MergeAdapter.GetItem")
}

// --- TESTS BELOW ---

func TestSingleAdapter(t *testing.T) {
	dummy := NewDummyAdapter([]int{1, 2, 3})
	merge := NewMergeAdapter(dummy)

	if count := merge.GetCount(); count != 3 {
		t.Errorf("Count should equal original size, got %d, want 3", count)
	}
	if val := merge.GetItem(0); val != 1 {
		t.Errorf("First item should be 1, got %d", val)
	}
	if val := merge.GetItem(1); val != 2 {
		t.Errorf("Second item should be 2, got %d", val)
	}
	if val := merge.GetItem(2); val != 3 {
		t.Errorf("Third item should be 3, got %d", val)
	}
}

func TestMultipleAdapters(t *testing.T) {
	dummy := NewDummyAdapter([]int{10, 20})
	dummy2 := NewDummyAdapter([]int{30})
	merge := NewMergeAdapter()
	merge.AddAdapter(dummy)
	merge.AddAdapter(dummy2)

	if count := merge.GetCount(); count != 3 {
		t.Errorf("Count should be sum of counts, got %d, want 3", count)
	}
	if val := merge.GetItem(0); val != 10 {
		t.Errorf("First item should be 10, got %d", val)
	}
	if val := merge.GetItem(1); val != 20 {
		t.Errorf("Second item should be 20, got %d", val)
	}
	if val := merge.GetItem(2); val != 30 {
		t.Errorf("Third item should be 30, got %d", val)
	}
}