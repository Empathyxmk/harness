package presenters

import (
	"testing"
)

type Counter struct {
	id    int
	name  string
	value int
}

func (c *Counter) SetId(id int)    { c.id = id }
func (c *Counter) GetId() int      { return c.id }
func (c *Counter) SetName(n string) { c.name = n }
func (c *Counter) GetName() string { return c.name }
func (c *Counter) SetValue(v int)  { c.value = v }
func (c *Counter) GetValue() int   { return c.value }

type CounterViewStub struct {
	NameSet       string
	ValueSet      int
	MinusEnabled  bool
	PlusEnabled   bool
	GoToDetail    *Counter
}

type CounterPresenter struct {
	view   *CounterViewStub
	model  *Counter
}

func (p *CounterPresenter) BindView(view *CounterViewStub) {
	p.view = view
}
func (p *CounterPresenter) SetModel(c *Counter) {
	p.model = c
	// Simulate view updates
	if p.view != nil {
		p.view.NameSet = c.GetName()
		p.view.ValueSet = c.GetValue()
		p.view.MinusEnabled = (c.GetValue() > 0)
		p.view.PlusEnabled = (c.GetValue() < 99)
	}
}
func (p *CounterPresenter) OnMinusButtonClicked() {
	if p.model != nil && p.model.GetValue() > 0 {
		p.model.SetValue(p.model.GetValue() - 1)
	}
}
func (p *CounterPresenter) OnPlusButtonClicked() {
	if p.model != nil && p.model.GetValue() < 99 {
		p.model.SetValue(p.model.GetValue() + 1)
	}
}
func (p *CounterPresenter) OnCounterClicked() {
	if p.view != nil {
		p.view.GoToDetail = p.model
	}
}

func TestCounterPresenter_UpdateView_setsName(t *testing.T) {
	ctr := &Counter{}
	ctr.SetId(4)
	ctr.SetName("My Counter")
	ctr.SetValue(18)
	view := &CounterViewStub{}
	pres := &CounterPresenter{}
	pres.BindView(view)
	pres.SetModel(ctr)
	if view.NameSet != "My Counter" {
		t.Errorf("expected name set, got %s", view.NameSet)
	}
}

func TestCounterPresenter_UpdateView_setsValue(t *testing.T) {
	ctr := &Counter{}
	ctr.SetValue(18)
	view := &CounterViewStub{}
	pres := &CounterPresenter{}
	pres.BindView(view)
	pres.SetModel(ctr)
	if view.ValueSet != 18 {
		t.Errorf("expected value set to 18, got %d", view.ValueSet)
	}
}

func TestCounterPresenter_UpdateView_WhenCounterGreaterThan0_setsMinusButtonEnabled(t *testing.T) {
	ctr := &Counter{}
	ctr.SetValue(1)
	view := &CounterViewStub{}
	pres := &CounterPresenter{}
	pres.BindView(view)
	pres.SetModel(ctr)
	if !view.MinusEnabled {
		t.Errorf("Minus button not enabled")
	}
}

func TestCounterPresenter_UpdateView_WhenCounterEqual0_setsMinusButtonDisabled(t *testing.T) {
	ctr := &Counter{}
	ctr.SetValue(0)
	view := &CounterViewStub{}
	pres := &CounterPresenter{}
	pres.BindView(view)
	pres.SetModel(ctr)
	if view.MinusEnabled {
		t.Errorf("Minus button not disabled")
	}
}

func TestCounterPresenter_UpdateView_WhenCounterLowerThan99_setsPlusButtonEnabled(t *testing.T) {
	ctr := &Counter{}
	ctr.SetValue(10)
	view := &CounterViewStub{}
	pres := &CounterPresenter{}
	pres.BindView(view)
	pres.SetModel(ctr)
	if !view.PlusEnabled {
		t.Errorf("Plus button not enabled")
	}
}

func TestCounterPresenter_UpdateView_WhenCounterEqual99_setsMinusButtonDisabled(t *testing.T) {
	ctr := &Counter{}
	ctr.SetValue(99)
	view := &CounterViewStub{}
	pres := &CounterPresenter{}
	pres.BindView(view)
	pres.SetModel(ctr)
	if view.PlusEnabled {
		t.Errorf("Plus button not disabled at 99")
	}
}

func TestCounterPresenter_OnMinusButtonClicked_WhenCounterGreaterThan0_decrementsValue(t *testing.T) {
	ctr := &Counter{}
	ctr.SetValue(16)
	pres := &CounterPresenter{}
	pres.SetModel(ctr)
	pres.OnMinusButtonClicked()
	if ctr.GetValue() != 15 {
		t.Errorf("Expected value 15, got %d", ctr.GetValue())
	}
}

func TestCounterPresenter_OnMinusButtonClicked_WhenCounterEquals0_doesNotDoAnything(t *testing.T) {
	ctr := &Counter{}
	ctr.SetValue(0)
	pres := &CounterPresenter{}
	pres.SetModel(ctr)
	pres.OnMinusButtonClicked()
	if ctr.GetValue() != 0 {
		t.Errorf("Should not decrement below 0")
	}
}

func TestCounterPresenter_OnPlusButtonClicked_WhenCounterLowerThan99_incrementsValue(t *testing.T) {
	ctr := &Counter{}
	ctr.SetValue(16)
	pres := &CounterPresenter{}
	pres.SetModel(ctr)
	pres.OnPlusButtonClicked()
	if ctr.GetValue() != 17 {
		t.Errorf("Expected value 17, got %d", ctr.GetValue())
	}
}

func TestCounterPresenter_OnPlusButtonClicked_WhenCounterEquals99_doesNotDoAnything(t *testing.T) {
	ctr := &Counter{}
	ctr.SetValue(99)
	pres := &CounterPresenter{}
	pres.SetModel(ctr)
	pres.OnPlusButtonClicked()
	if ctr.GetValue() != 99 {
		t.Errorf("Value should stay at 99, got %d", ctr.GetValue())
	}
}

func TestCounterPresenter_OnCounterClicked_opensDetailView(t *testing.T) {
	ctr := &Counter{}
	view := &CounterViewStub{}
	pres := &CounterPresenter{}
	pres.BindView(view)
	pres.SetModel(ctr)
	pres.OnCounterClicked()
	if view.GoToDetail != ctr {
		t.Errorf("GoToDetailView not called correctly")
	}
}