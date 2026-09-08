package original

import (
	"testing"
)

// Dummy implementations for interfaces
type DummyFileChooseInterceptor struct{}

func (d *DummyFileChooseInterceptor) OnFileChosen(sel []string, orig bool, code int, action interface{}) bool {
	return sel != nil && len(sel) > 0 && orig && code == 2 && action == nil
}

func (d *DummyFileChooseInterceptor) DescribeContents() int {
	return 0
}

func (d *DummyFileChooseInterceptor) WriteToParcel(_ interface{}, _ int) {}

func TestFileChooseInterceptor_OnFileChosen(t *testing.T) {
	impl := &DummyFileChooseInterceptor{}
	sel := []string{"pic1"}
	if !impl.OnFileChosen(sel, true, 2, nil) {
		t.Error("Expected OnFileChosen to return true")
	}
}

func TestFileChooseInterceptor_Parcelable(t *testing.T) {
	impl := &DummyFileChooseInterceptor{}
	if impl.DescribeContents() != 0 {
		t.Error("Expected DescribeContents to return 0")
	}
	impl.WriteToParcel(nil, 0)
	arr := make([]*DummyFileChooseInterceptor, 3)
	if len(arr) != 3 {
		t.Errorf("Expected array length 3, got %d", len(arr))
	}
	inst := &DummyFileChooseInterceptor{}
	if inst == nil {
		t.Error("Expected non-nil instance")
	}
}