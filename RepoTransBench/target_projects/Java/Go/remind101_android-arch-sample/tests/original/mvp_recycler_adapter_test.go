package original

import (
	"testing"
)

type DummyModel struct {
	ID int
}

type DummyPresenter2 struct {
}

type DummyVHolder struct {
	wasBound   bool
	wasUnbound bool
	Presenter  *DummyPresenter2
}

func (vh *DummyVHolder) BindPresenter(p *DummyPresenter2) {
	vh.wasBound = true
	vh.Presenter = p
}

func (vh *DummyVHolder) UnbindPresenter() {
	vh.wasUnbound = true
	vh.Presenter = nil
}

// DummyAdapter is a mock adapter for testing
type DummyAdapter struct {
	models    []DummyModel
	presenters map[int]*DummyPresenter2
}

func NewDummyAdapter(models []DummyModel) *DummyAdapter {
	adapter := &DummyAdapter{
		models:     models,
		presenters: make(map[int]*DummyPresenter2),
	}
	for _, m := range models {
		adapter.presenters[m.ID] = &DummyPresenter2{}
	}
	return adapter
}

func (a *DummyAdapter) GetPresenter(m DummyModel) *DummyPresenter2 {
	return a.presenters[m.ID]
}
func (a *DummyAdapter) OnBindViewHolder(holder *DummyVHolder, pos int) {
	p := a.GetPresenter(a.models[pos])
	holder.BindPresenter(p)
}
func (a *DummyAdapter) OnViewRecycled(holder *DummyVHolder) {
	holder.UnbindPresenter()
}

func (a *DummyAdapter) OnFailedToRecycleView(holder *DummyVHolder) bool {
	holder.UnbindPresenter()
	return false
}

func TestMvpRecyclerAdapter_GetPresenterReturnsCorrectPresenter(t *testing.T) {
	models := []DummyModel{{ID: 1}, {ID: 2}}
	adapter := NewDummyAdapter(models)
	m := DummyModel{ID: 1}
	p := adapter.GetPresenter(m)
	if p == nil {
		t.Fatalf("GetPresenter returned nil")
	}
}

func TestMvpRecyclerAdapter_OnBindViewHolderBindsPresenter(t *testing.T) {
	models := []DummyModel{{ID: 1}, {ID: 2}}
	adapter := NewDummyAdapter(models)
	holder := &DummyVHolder{}
	adapter.OnBindViewHolder(holder, 0)
	if !holder.wasBound {
		t.Errorf("BindPresenter was not called")
	}
}

func TestMvpRecyclerAdapter_OnViewRecycledUnbindsPresenter(t *testing.T) {
	adapter := NewDummyAdapter([]DummyModel{{ID: 1}})
	holder := &DummyVHolder{}
	adapter.OnViewRecycled(holder)
	if !holder.wasUnbound {
		t.Errorf("UnbindPresenter was not called")
	}
}

func TestMvpRecyclerAdapter_OnFailedToRecycleViewUnbindsPresenter(t *testing.T) {
	adapter := NewDummyAdapter([]DummyModel{{ID: 1}})
	holder := &DummyVHolder{}
	result := adapter.OnFailedToRecycleView(holder)
	if !holder.wasUnbound {
		t.Errorf("UnbindPresenter not called in OnFailedToRecycleView")
	}
	if result != false {
		t.Errorf("Expected false return from OnFailedToRecycleView")
	}
}