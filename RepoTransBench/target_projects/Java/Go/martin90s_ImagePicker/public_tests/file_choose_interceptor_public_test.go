package public_tests

import (
	"testing"
)

type DummyImplPublic struct{}

func (d *DummyImplPublic) OnFileChosen(sel []string, orig bool, code int, action interface{}) bool {
	return sel != nil && len(sel) > 1 && !orig && code == 5 && action != nil
}

func (d *DummyImplPublic) DescribeContents() int {
	return 0
}
func (d *DummyImplPublic) WriteToParcel(_ interface{}, _ int) {}

func TestFileChooseInterceptor_OnFileChosenWithDifferentData(t *testing.T) {
	impl := &DummyImplPublic{}
	sel := []string{"picA", "picB"}
	if !impl.OnFileChosen(sel, false, 5, struct{}{}) {
		t.Error("Expected OnFileChosen to return true with public test data")
	}
}

func TestFileChooseInterceptor_ParcelableDifferentSize(t *testing.T) {
	impl := &DummyImplPublic{}
	if impl.DescribeContents() != 0 {
		t.Error("Expected DescribeContents to return 0")
	}
	impl.WriteToParcel(nil, 0)
	arr := make([]*DummyImplPublic, 2)
	if len(arr) != 2 {
		t.Errorf("Expected array length 2")
	}
	inst := &DummyImplPublic{}
	if inst == nil {
		t.Error("Expected non-nil instance")
	}
}