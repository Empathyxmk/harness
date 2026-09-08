package public_tests

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

func TestSingleAdapterDifferentData(t *testing.T) {
	dummy := NewDummyAdapter([]int{42, 7, 18})
	merge := NewMergeAdapter(dummy)

	if count := merge.GetCount(); count != 3 {
		t.Errorf("Count should equal original size, got %d, want 3", count)
	}
	if val := merge.GetItem(0); val != 42 {
		t.Errorf("First item should be 42, got %d", val)
	}
	if val := merge.GetItem(1); val != 7 {
		t.Errorf("Second item should be 7, got %d", val)
	}
	if val := merge.GetItem(2); val != 18 {
		t.Errorf("Third item should be 18, got %d", val)
	}
}

func TestMultipleAdaptersDifferentData(t *testing.T) {
	dummyA := NewDummyAdapter([]int{91, 22})
	dummyB := NewDummyAdapter([]int{55, 66})
	merge := NewMergeAdapter()
	merge.AddAdapter(dummyA)
	merge.AddAdapter(dummyB)

	if count := merge.GetCount(); count != 4 {
		t.Errorf("Count should be sum of counts, got %d, want 4", count)
	}
	if val := merge.GetItem(0); val != 91 {
		t.Errorf("First item should be 91, got %d", val)
	}
	if val := merge.GetItem(1); val != 22 {
		t.Errorf("Second item should be 22, got %d", val)
	}
	if val := merge.GetItem(2); val != 55 {
		t.Errorf("Third item should be 55, got %d", val)
	}
	if val := merge.GetItem(3); val != 66 {
		t.Errorf("Fourth item should be 66, got %d", val)
	}
}