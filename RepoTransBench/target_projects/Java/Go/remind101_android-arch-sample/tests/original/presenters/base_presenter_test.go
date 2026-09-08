package presenters

import (
	"testing"
)

type DummyView struct {
	Val int
}

type DummyPresenter struct {
	view *DummyView
}

func (p *DummyPresenter) BindView(v *DummyView) {
	p.view = v
}
func (p *DummyPresenter) UnbindView() {
	p.view = nil
}
func (p *DummyPresenter) GetView() *DummyView {
	return p.view
}

func TestBasePresenter_BindViewAndUnbindView(t *testing.T) {
	p := &DummyPresenter{}
	v := &DummyView{Val: 123}
	p.BindView(v)
	if p.GetView() == nil {
		t.Fatalf("Expected view to be bound")
	}
	p.UnbindView()
	if p.GetView() != nil {
		t.Errorf("Expected view to be nil after unbind")
	}
}