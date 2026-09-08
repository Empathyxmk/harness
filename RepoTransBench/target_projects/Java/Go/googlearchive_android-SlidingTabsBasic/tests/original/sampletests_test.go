package tests

import (
	"testing"
)

type MainActivity struct {
	fragments []interface{}
}

func (a *MainActivity) GetSupportFragmentManager() *FragmentManager {
	return &FragmentManager{fragments: a.fragments}
}
type FragmentManager struct {
	fragments []interface{}
}
func (f *FragmentManager) GetFragments() []interface{} {
	return f.fragments
}

type SlidingTabsBasicFragment struct{}

func TestSampleTestsPreconditions(t *testing.T) {
	activity := &MainActivity{
		fragments: []interface{}{&SlidingTabsBasicFragment{}, &SlidingTabsBasicFragment{}},
	}
	copiedFragment := activity.GetSupportFragmentManager().GetFragments()[1]
	if activity == nil {
		t.Errorf("mTestActivity is null")
	}
	if copiedFragment == nil {
		t.Errorf("mTestFragment is null")
	}
}