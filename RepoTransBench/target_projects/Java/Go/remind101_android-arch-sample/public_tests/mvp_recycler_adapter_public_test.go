package public_tests

import "testing"

type TestModel struct {
	Value int
}
type TestPresenter struct{}

type TestViewHolder struct {
	bound        bool
	unbound      bool
	lastPresenter *TestPresenter
}

func (vh *TestViewHolder) BindPresenter(p *TestPresenter) {
	vh.bound = true
	vh.lastPresenter = p
}
func (vh *TestViewHolder) UnbindPresenter() {
	vh.unbound = true
	vh.lastPresenter = nil
}

type TestAdapter struct {
	items      []TestModel
	presenters map[int]*TestPresenter
}

func NewTestAdapter(items []TestModel) *TestAdapter {
	ad := &TestAdapter{items: items, presenters: map[int]*TestPresenter{}}
	for _, m := range items {
		ad.presenters[m.Value] = &TestPresenter{}
	}
	return ad
}

func (ad *TestAdapter) OnBindViewHolder(vh *TestViewHolder, position int) {
	m := ad.items[position]
	p := ad.presenters[m.Value]
	vh.BindPresenter(p)
}
func (ad *TestAdapter) OnViewRecycled(vh *TestViewHolder) {
	vh.UnbindPresenter()
}
func (ad *TestAdapter) OnFailedToRecycleView(vh *TestViewHolder) bool {
	vh.UnbindPresenter()
	return false
}

func TestMvpRecyclerAdapterPublicTest_BindAndUnbindPresenterWithDifferentModelData(t *testing.T) {
	model := TestModel{Value: 100}
	adapter := NewTestAdapter([]TestModel{model})
	holder := &TestViewHolder{}
	adapter.OnBindViewHolder(holder, 0)
	if !holder.bound {
		t.Errorf("BindPresenter not called")
	}
	if holder.lastPresenter == nil {
		t.Errorf("lastPresenter not set")
	}
	adapter.OnViewRecycled(holder)
	if !holder.unbound {
		t.Errorf("UnbindPresenter not called")
	}
	if holder.lastPresenter != nil {
		t.Errorf("lastPresenter not reset")
	}
}

func TestMvpRecyclerAdapterPublicTest_OnFailedToRecycleViewCallsUnbindWithDifferentModel(t *testing.T) {
	model := TestModel{Value: 997}
	adapter := NewTestAdapter([]TestModel{model})
	holder := &TestViewHolder{}
	res := adapter.OnFailedToRecycleView(holder)
	if !holder.unbound {
		t.Errorf("UnbindPresenter not called")
	}
	if res != false {
		t.Errorf("Expected false return from OnFailedToRecycleView")
	}
}