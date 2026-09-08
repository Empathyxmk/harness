package original

import (
	"testing"
)

type DummyBasePresenter struct {
	BinderWasCalled bool
}

func (bp *DummyBasePresenter) BindView(view interface{}) {
	bp.BinderWasCalled = true
}

type DummyViewHolder struct {
	Presenter *DummyBasePresenter
}

func (vh *DummyViewHolder) BindPresenter(p *DummyBasePresenter) {
	vh.Presenter = p
	if p != nil {
		p.BindView(vh)
	}
}

func (vh *DummyViewHolder) UnbindPresenter() {
	vh.Presenter = nil
}

func TestViewHolder_BindAndUnbindPresenter(t *testing.T) {
	p := &DummyBasePresenter{}
	vh := &DummyViewHolder{}
	vh.BindPresenter(p)
	if vh.Presenter != p {
		t.Errorf("Presenter wasn't bound correctly")
	}
	if !p.BinderWasCalled {
		t.Errorf("Presenter bind was not called")
	}
	vh.UnbindPresenter()
	if vh.Presenter != nil {
		t.Errorf("Presenter was not unbound")
	}
}