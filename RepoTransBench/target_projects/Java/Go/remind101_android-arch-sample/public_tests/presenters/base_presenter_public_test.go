package presenters

import "testing"

type DummyPublicPresenter struct {
	view string
	attached bool
}

func (p *DummyPublicPresenter) AttachView(v string) {
	p.view = v
	p.attached = true
}
func (p *DummyPublicPresenter) DetachView() {
	p.view = ""
	p.attached = false
}
func (p *DummyPublicPresenter) IsViewAttached() bool {
	return p.attached
}
func (p *DummyPublicPresenter) GetView() string {
	return p.view
}

func TestBasePresenterPublic_AttachAndDetachViewPublic(t *testing.T) {
	p := &DummyPublicPresenter{}
	view := "PUBLIC_TEST_VIEW"
	p.AttachView(view)
	if !p.IsViewAttached() {
		t.Errorf("Expected view attached")
	}
	if p.GetView() != view {
		t.Errorf("Got wrong view: %s", p.GetView())
	}
	p.DetachView()
	if p.IsViewAttached() {
		t.Errorf("Expected view detached")
	}
	if p.GetView() != "" {
		t.Errorf("View should be empty after detach")
	}
}