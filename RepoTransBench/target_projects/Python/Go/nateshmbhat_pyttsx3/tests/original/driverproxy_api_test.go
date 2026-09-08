package original

import (
	"reflect"
	"testing"
)

// DummyDriver mimics a speech driver for driverproxy tests
type DummyDriver struct {
	Destroyed   bool
	TextSpoken  string
	SayCalled   []string
	Busy        bool
	Stopped     bool
}

func (d *DummyDriver) Destroy() bool {
	d.Destroyed = true
	return true
}
func (d *DummyDriver) Say(text string) {
	d.TextSpoken = text
	d.SayCalled = append(d.SayCalled, text)
}
func (d *DummyDriver) Stop() string {
	d.Stopped = true
	return "stopped"
}

// DummyEngine mimics an engine for driverproxy tests
type DummyEngine struct {
	Notifications []Notification
}
type Notification struct {
	Topic string
	Kw    map[string]interface{}
}
func (e *DummyEngine) Notify(topic string, kw map[string]interface{}) {
	e.Notifications = append(e.Notifications, Notification{Topic: topic, Kw: kw})
}

// DriverProxy mimics the main wrapper for a pyttsx3-like backend system
type DriverProxy struct {
	Driver *DummyDriver
	Engine *DummyEngine
	Busy   bool
	Queue  []QueuedFunc
	Name   string
}
type QueuedFunc struct {
	Fn   func(...interface{})
	Args []interface{}
	Name string
}
func DummyImportBuildDriver(_ string, proxy *DriverProxy) *DummyDriver {
	return &DummyDriver{Busy: true}
}
func NewDriverProxy(engine *DummyEngine, name string, debug bool) *DriverProxy {
	return &DriverProxy{
		Driver: DummyImportBuildDriver(name, nil),
		Engine: engine,
		Busy:   true,
		Queue:  make([]QueuedFunc, 0),
	}
}
func (p *DriverProxy) Destroy() {
	p.Driver.Destroy()
}
func (p *DriverProxy) Del() {
	p.Destroy()
}
func (p *DriverProxy) Push(fn func(...interface{}), args []interface{}, name string) {
	// If not busy, call immediately, else queue
	if !p.Busy {
		fn(args...)
	} else {
		p.Queue = append(p.Queue, QueuedFunc{Fn: fn, Args: args, Name: name})
	}
}
func (p *DriverProxy) Notify(topic string, kw map[string]interface{}) {
	if kw == nil {
		kw = map[string]interface{}{}
	}
	kw["name"] = p.Name
	p.Engine.Notify(topic, kw)
}
func (p *DriverProxy) SetBusy(b bool) { p.Busy = b }
func (p *DriverProxy) IsBusy() bool   { return p.Busy }
func (p *DriverProxy) Say(text, tid string) {
	p.Driver.Say(text)
}
func (p *DriverProxy) Stop() { p.Driver.Stop() }

func TestDriverProxyInit(t *testing.T) {
	eng := &DummyEngine{}
	p := NewDriverProxy(eng, "dummy", false)
	if reflect.TypeOf(p.Driver).Elem().Name() != "DummyDriver" {
		t.Errorf("Driver is wrong type, got %T", p.Driver)
	}
	if p.Engine != eng {
		t.Errorf("Engine not set")
	}
	if !p.Busy {
		t.Errorf("Should be busy at init")
	}
	if len(p.Queue) != 0 {
		t.Errorf("Queue should be empty at init")
	}
}

func TestDriverProxyDel(t *testing.T) {
	called := false
	type DummyDrv struct{ DummyDriver }
	var d DummyDrv
	d.Destroyed = false
	engine := &DummyEngine{}
	p := &DriverProxy{
		Driver: &d.DummyDriver,
		Engine: engine,
		Busy:   true,
		Queue:  []QueuedFunc{},
	}
	p.Del()
	if !p.Driver.Destroyed {
		t.Errorf("Destroy not called on underlying driver")
	}
}

func TestDriverProxyPushAndPump(t *testing.T) {
	eng := &DummyEngine{}
	p := NewDriverProxy(eng, "dummy", true)
	p.Busy = false
	var called []string
	meth1 := func(args ...interface{}) {
		if len(args) == 1 {
			val, ok := args[0].(string)
			if ok {
				called = append(called, val)
			}
		}
	}
	p.Queue = []QueuedFunc{}
	p.Push(meth1, []interface{}{"hello"}, "tid")
	if len(called) != 1 || called[0] != "hello" {
		t.Errorf("Push did not call meth1 as expected, got %+v", called)
	}
}

func TestDriverProxyNotify(t *testing.T) {
	eng := &DummyEngine{}
	p := NewDriverProxy(eng, "dummy", false)
	p.Name = "abc"
	p.Notify("test_topic", map[string]interface{}{"foo": 123})
	last := eng.Notifications[len(eng.Notifications)-1]
	if last.Topic != "test_topic" {
		t.Errorf("Expected topic=test_topic, got %v", last.Topic)
	}
	if last.Kw["foo"] != 123 {
		t.Errorf("Expected foo=123, got %v", last.Kw["foo"])
	}
	if last.Kw["name"] != "abc" {
		t.Errorf("Expected name=abc, got %v", last.Kw["name"])
	}
}

func TestDriverProxySetBusyAndIsBusy(t *testing.T) {
	eng := &DummyEngine{}
	p := NewDriverProxy(eng, "dummy", false)
	p.SetBusy(false)
	if p.IsBusy() {
		t.Errorf("isBusy should be false after setBusy(false)")
	}
	p.SetBusy(true)
	if !p.IsBusy() {
		t.Errorf("isBusy should be true after setBusy(true)")
	}
}

func TestDriverProxySay(t *testing.T) {
	type DummyDrv struct {
		DummyDriver
	}
	var d DummyDrv
	eng := &DummyEngine{}
	p := &DriverProxy{
		Driver: &d.DummyDriver,
		Engine: eng,
		Busy:   false,
	}
	p.Say("abc", "tid")
	if p.Driver.TextSpoken != "abc" {
		t.Errorf("Say() did not set TextSpoken to abc")
	}
}

func TestDriverProxyStop(t *testing.T) {
	type DummyDrv struct {
		DummyDriver
	}
	var d DummyDrv
	eng := &DummyEngine{}
	p := &DriverProxy{
		Driver: &d.DummyDriver,
		Engine: eng,
		Queue:  []QueuedFunc{},
	}
	p.Stop()
	if !p.Driver.Stopped {
		t.Errorf("Stop should set Stopped") // basic check
	}
}