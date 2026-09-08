package presenters

import "testing"

type Counter struct {
	value int
}

func (c *Counter) SetValue(v int) { c.value = v }
func (c *Counter) GetValue() int  { return c.value }
func (c *Counter) Increment()     { c.value++ }
func (c *Counter) Decrement()     { c.value-- }

type DummyView struct {
	lastValue  int
	onIncrement bool
	onDecrement bool
}

type CounterPresenter struct {
	counter *Counter
	view    *DummyView
	attached bool
}

func NewCounterPresenter(counter *Counter) *CounterPresenter {
	return &CounterPresenter{counter: counter}
}
func (p *CounterPresenter) AttachView(v *DummyView) {
	p.view = v
	p.attached = true
}
func (p *CounterPresenter) DetachView() {
	p.attached = false
	p.view = nil
}
func (p *CounterPresenter) IsViewAttached() bool {
	return p.attached
}
func (p *CounterPresenter) Increment() {
	p.counter.Increment()
	if p.view != nil {
		p.view.lastValue = p.counter.GetValue()
		p.view.onIncrement = true
	}
}
func (p *CounterPresenter) Decrement() {
	p.counter.Decrement()
	if p.view != nil {
		p.view.lastValue = p.counter.GetValue()
		p.view.onDecrement = true
	}
}

func TestCounterPresenterPublic_IncrementPublic(t *testing.T) {
	counter := &Counter{}
	counter.SetValue(42)
	p := NewCounterPresenter(counter)
	view := &DummyView{}
	p.AttachView(view)
	p.Increment()
	if counter.GetValue() != 43 {
		t.Errorf("Expected counter value 43, got %d", counter.GetValue())
	}
	if view.lastValue != 43 {
		t.Errorf("View lastValue not updated")
	}
	if !view.onIncrement {
		t.Errorf("onIncrement was not true")
	}
}
func TestCounterPresenterPublic_DecrementPublic(t *testing.T) {
	counter := &Counter{}
	counter.SetValue(42)
	p := NewCounterPresenter(counter)
	view := &DummyView{}
	p.AttachView(view)
	p.Decrement()
	if counter.GetValue() != 41 {
		t.Errorf("Expected counter value 41, got %d", counter.GetValue())
	}
	if view.lastValue != 41 {
		t.Errorf("View lastValue not updated")
	}
	if !view.onDecrement {
		t.Errorf("onDecrement was not true")
	}
}
func TestCounterPresenterPublic_AttachDetachViewPublic(t *testing.T) {
	counter := &Counter{}
	p := NewCounterPresenter(counter)
	view := &DummyView{}
	p.AttachView(view)
	if !p.IsViewAttached() {
		t.Errorf("View should be attached")
	}
	p.DetachView()
	if p.IsViewAttached() {
		t.Errorf("View should be detached")
	}
}