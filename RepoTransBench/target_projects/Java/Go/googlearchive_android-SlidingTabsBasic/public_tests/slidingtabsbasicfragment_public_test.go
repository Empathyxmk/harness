package public_tests

import (
	"fmt"
	"testing"
)

type View struct {
	id       int
	findFunc func(id int) interface{}
}

func (v *View) FindViewById(id int) interface{} {
	if v.findFunc != nil {
		return v.findFunc(id)
	}
	return nil
}

type ViewPager struct {
	setAdapter func(adapter *SamplePagerAdapter)
}

func (vp *ViewPager) SetAdapter(adapter *SamplePagerAdapter) {
	if vp.setAdapter != nil {
		vp.setAdapter(adapter)
	}
}

type SlidingTabLayout struct {
	setViewPager func(vp *ViewPager)
}

func (stl *SlidingTabLayout) SetViewPager(vp *ViewPager) {
	if stl.setViewPager != nil {
		stl.setViewPager(vp)
	}
}

type SlidingTabsBasicFragment struct{}
type SamplePagerAdapter struct {
	customCount   int
	customGetPage func(i int) string
}

func (a *SamplePagerAdapter) GetCount() int {
	if a.customCount > 0 {
		return a.customCount
	}
	return 10
}
func (a *SamplePagerAdapter) IsViewFromObject(v1 *View, obj interface{}) bool {
	return v1 == obj
}
func (a *SamplePagerAdapter) GetPageTitle(i int) string {
	if a.customGetPage != nil {
		return a.customGetPage(i)
	}
	return "Item " + itoa(i+1)
}
func itoa(i int) string { return fmt.Sprintf("%d", i) }

type LayoutInflater struct {
	inflateFunc func(resID int, container *ViewGroup, attachToRoot bool) *View
}
type ViewGroup struct{ View }

func (li *LayoutInflater) Inflate(resID int, container *ViewGroup, attachToRoot bool) *View {
	if li.inflateFunc != nil {
		return li.inflateFunc(resID, container, attachToRoot)
	}
	return &View{}
}
type Bundle struct{}

func (f *SlidingTabsBasicFragment) OnCreateView(inflater *LayoutInflater, container *ViewGroup, bundle *Bundle) *View {
	return inflater.Inflate(123456, container, false)
}
func (f *SlidingTabsBasicFragment) OnViewCreated(view *View, _ interface{}) {
	// for test, simulate setAdapter/setViewPager being called if available (no-op)
	if pager, ok := view.FindViewById(777).(*ViewPager); ok {
		pager.SetAdapter(&SamplePagerAdapter{})
	}
	if tabLayout, ok := view.FindViewById(888).(*SlidingTabLayout); ok {
		tabLayout.SetViewPager(&ViewPager{})
	}
}

func TestOnCreateViewInflatesDifferentView(t *testing.T) {
	fragment := &SlidingTabsBasicFragment{}
	fakeView := &View{id: 999}
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

func TestOnViewCreatedWithDifferentMocks(t *testing.T) {
	fragment := &SlidingTabsBasicFragment{}
	setAdapterFlag := false
	setViewPagerFlag := false
	pager := &ViewPager{setAdapter: func(adapter *SamplePagerAdapter) { setAdapterFlag = true }}
	tabLayout := &SlidingTabLayout{setViewPager: func(vp *ViewPager) { setViewPagerFlag = true }}
	view := &View{findFunc: func(id int) interface{} {
		if id == 777 {
			return pager
		}
		if id == 888 {
			return tabLayout
		}
		return nil
	}}
	fragment.OnViewCreated(view, nil)
	if !setAdapterFlag {
		t.Errorf("SetAdapter (public) not called")
	}
	if !setViewPagerFlag {
		t.Errorf("SetViewPager (public) not called")
	}
}

func TestSamplePagerAdapterGetCountIsElevenPublic(t *testing.T) {
	adapter := &SamplePagerAdapter{customCount: 11}
	if adapter.GetCount() != 11 {
		t.Errorf("Expected count=11, got %d", adapter.GetCount())
	}
}

func TestIsViewFromObjectDifferentObjects(t *testing.T) {
	adapter := &SamplePagerAdapter{}
	v1 := &View{id: 1}
	v2 := &View{id: 2}
	if adapter.IsViewFromObject(v1, v2) {
		t.Errorf("Diff objects should return false")
	}
	if !adapter.IsViewFromObject(v2, v2) {
		t.Errorf("Same object not true")
	}
}

func TestGetPageTitlePublic(t *testing.T) {
	adapter := &SamplePagerAdapter{
		customCount: 3,
		customGetPage: func(i int) string {
			return "Tab " + itoa(i*2)
		},
	}
	for i := 0; i < adapter.GetCount(); i++ {
		if adapter.GetPageTitle(i) != "Tab "+itoa(i*2) {
			t.Errorf("Custom title mismatch: %s (got) vs %s (want)", adapter.GetPageTitle(i), "Tab "+itoa(i*2))
		}
	}
}