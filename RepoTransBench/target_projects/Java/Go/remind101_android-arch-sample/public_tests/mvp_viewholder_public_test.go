package public_tests

import "testing"

type DummyPublicPresenter struct{}

type DummyPublicViewHolder struct {
	bindCalled    bool
	unbindCalled  bool
	boundPresenter *DummyPublicPresenter
}

func (vh *DummyPublicViewHolder) BindPresenter(p *DummyPublicPresenter) {
	vh.bindCalled = true
	vh.boundPresenter = p
}
func (vh *DummyPublicViewHolder) UnbindPresenter() {
	vh.unbindCalled = true
	vh.boundPresenter = nil
}

func TestMvpViewHolderPublicTest_BindAndUnbindPresenterPublic(t *testing.T) {
	presenter := &DummyPublicPresenter{}
	vh := &DummyPublicViewHolder{}
	vh.BindPresenter(presenter)
	if !vh.bindCalled {
		t.Errorf("bindCalled not set")
	}
	if vh.boundPresenter != presenter {
		t.Errorf("Presenter not bound correctly")
	}
	vh.UnbindPresenter()
	if !vh.unbindCalled {
		t.Errorf("unbindCalled not set")
	}
	if vh.boundPresenter != nil {
		t.Errorf("Presenter reference not cleared")
	}
}