package tests

import (
	"testing"
)

type SamplePagerAdapter struct {count int}

func (a *SamplePagerAdapter) GetCount() int { return 10 }
func (a *SamplePagerAdapter) IsViewFromObject(v *View, obj interface{}) bool {
	return v == obj
}
func (a *SamplePagerAdapter) GetPageTitle(i int) string {
	return "Item " + itoa(i+1)
}
func itoa(i int) string { return fmt.Sprintf("%d", i) }

type SlidingTabsBasicFragment struct{}
func (f *SlidingTabsBasicFragment) OnCreateView(inflater *LayoutInflater, container *ViewGroup, bundle *Bundle) *View {
	return inflater.Inflate(383, container, false)
}
func (f *SlidingTabsBasicFragment) OnViewCreated(view *View, _ interface{}) {
	pager := view.FindViewById(R.ViewPager)
	tabLayout := view.FindViewById(R.SlidingTabs)
	if vp, ok := pager.(*ViewPager); ok {
		vp.SetAdapter(&SamplePagerAdapter{})
	}
	if tl, ok := tabLayout.(*SlidingTabLayout); ok {
		tl.SetViewPager(&ViewPager{})
	}
}

func TestOnCreateViewInflates(t *testing.T) {
	fragment := &SlidingTabsBasicFragment{}
	fakeView := &View{}
	inflater := &LayoutInflater{inflateFunc: func(resID int, container *ViewGroup, attachToRoot bool) *View {
		return fakeView
	}}
	container := &ViewGroup{}
	bundle := &Bundle{}
	res := fragment.OnCreateView(inflater, container, bundle)
	if res != fakeView {
		t.Errorf("Expected fakeView, got %+v", res)
	}
}

func TestOnViewCreated(t *testing.T) {
	fragment := &SlidingTabsBasicFragment{}
	pager := &ViewPager{}
	tabLayout := &SlidingTabLayout{}
	setAdapterCalled := false
	pager.setAdapter = func(adapter *SamplePagerAdapter) { setAdapterCalled = true }
	setViewPagerCalled := false
	tabLayout.setViewPager = func(vp *ViewPager) { setViewPagerCalled = true }

	view := &View{
		findFunc: func(id int) interface{} {
			if id == R.ViewPager { return pager }
			if id == R.SlidingTabs { return tabLayout }
			return nil
		},
	}
	fragment.OnViewCreated(view, nil)
	if !setAdapterCalled {
		t.Errorf("pager.SetAdapter not called")
	}
	if !setViewPagerCalled {
		t.Errorf("tabLayout.SetViewPager not called")
	}
}

func TestSamplePagerAdapterGetCountIsTen(t *testing.T) {
	adapter := &SamplePagerAdapter{}
	if adapter.GetCount() != 10 {
		t.Errorf("Expected count=10, got %d", adapter.GetCount())
	}
}

func TestIsViewFromObject(t *testing.T) {
	v := &View{}
	adapter := &SamplePagerAdapter{}
	if !adapter.IsViewFromObject(v, v) {
		t.Errorf("Same object should return true")
	}
	if adapter.IsViewFromObject(&View{}, &struct{}{}) {
		t.Errorf("Diff objects returns true wrongly")
	}
}

func TestGetPageTitle(t *testing.T) {
	adapter := &SamplePagerAdapter{}
	for i := 0; i < adapter.GetCount(); i++ {
		if adapter.GetPageTitle(i) != "Item "+itoa(i+1) {
			t.Errorf("Title mismatch: %s", adapter.GetPageTitle(i))
		}
	}
}