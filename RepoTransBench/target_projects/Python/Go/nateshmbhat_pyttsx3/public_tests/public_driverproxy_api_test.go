package public_tests

import (
	"reflect"
	"testing"
)

// --- Types as in public python tests ---

type AnotherDummyEngine struct {
	Notified []Notification
}
type Notification struct {
	Topic string
	Kw    map[string]interface{}
}
func (e *AnotherDummyEngine) Notify(topic string, kw map[string]interface{}) {
	e.Notified = append(e.Notified, Notification{Topic: topic, Kw: kw})
}

type AnotherDummyDriver struct {
	Proxy    *DriverProxy
	Said     [][2]string
	Stopped  bool
	Busy     *bool
	SaidItems [][2]string
	TimesStopped int
}
func (d *AnotherDummyDriver) StartLoop()            {}
func (d *AnotherDummyDriver) EndLoop()              {}
func (d *AnotherDummyDriver) Say(text, name string) { d.Said = append(d.Said, [2]string{text, name}) }
func (d *AnotherDummyDriver) Stop()                 { d.Stopped = true; d.TimesStopped += 1 }
func (d *AnotherDummyDriver) SetBusy(b bool)        { d.Busy = &b }
func (d *AnotherDummyDriver) NotifyIt(data interface{}) {}

// ---- DriverProxy ----

type QueuedFunc struct {
	Fn   func(...interface{}) interface{}
	Args []interface{}
	Name string
}
type DriverProxy struct {
	Engine *AnotherDummyEngine
	Driver *AnotherDummyDriver
	Busy   bool
	Queue  []QueuedFunc
	Name   string
}
func NewDriverProxyPublic(engine *AnotherDummyEngine, name string) *DriverProxy {
	return &DriverProxy{
		Engine: engine,
		Driver: &AnotherDummyDriver{},
		Busy:   true,
		Queue:  make([]QueuedFunc, 0),
		Name:   name,
	}
}
func (p *DriverProxy) Push(fn func(...interface{}) interface{}, args []interface{}, name string) {
	p.Queue = append(p.Queue, QueuedFunc{Fn: fn, Args: args, Name: name})
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
func (p *DriverProxy) Say(text, name string) {
	// Emulate queued call
	p.Queue = append(p.Queue, QueuedFunc{
		Fn: func(args ...interface{}) interface{} {
			p.Driver.Say(text, name)
			return nil
		}, Args: []interface{}{text, name}, Name: name,
	})
}
func (p *DriverProxy) Stop() {
	p.Queue = append(p.Queue, QueuedFunc{
		Fn: func(args ...interface{}) interface{} {
			p.Driver.Stop()
			return nil
		}, Args: []interface{}{}, Name: "",
	})
}
func (p *DriverProxy) Del() {
	p.Driver.Stopped = true // as placeholder for del/destroy
}

func TestPublicDriverproxyInit(t *testing.T) {
	eng := &AnotherDummyEngine{}
	proxy := NewDriverProxyPublic(eng, "otherdummy")
	if reflect.TypeOf(proxy.Driver).Elem().Name() != "AnotherDummyDriver" {
		t.Errorf("Wrong driver type on init")
	}
	if proxy.Engine != eng {
		t.Errorf("Engine not set")
	}
	if !proxy.Busy {
		t.Errorf("Should be busy by default")
	}
}

func TestPublicDriverproxyDel(t *testing.T) {
	proxy := NewDriverProxyPublic(&AnotherDummyEngine{}, "del")
	defer func() {
		if v := recover(); v != nil {
			t.Errorf("del raised panic: %v", v)
		}
	}()
	proxy.Del() // Should not panic
	if !proxy.Driver.Stopped {
		t.Errorf("Driver.Del did not set stopped to true")
	}
}

func TestPublicDriverproxyPushAndPump(t *testing.T) {
	proxy := NewDriverProxyPublic(&AnotherDummyEngine{}, "push")
	proxy.Push(func(args ...interface{}) interface{} {
		return args[0].(string) + "X"
	}, []interface{}{"fox"}, "")
	proxy.Push(func(args ...interface{}) interface{} {
		// Reverse string
		s := args[0].(string)
		runes := []rune(s)
		for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
			runes[i], runes[j] = runes[j], runes[i]
		}
		return string(runes)
	}, []interface{}{"bottle"}, "")
	collected := []interface{}{}
	for len(proxy.Queue) > 0 {
		qf := proxy.Queue[0]
		proxy.Queue = proxy.Queue[1:]
		collected = append(collected, qf.Fn(qf.Args...))
	}
	if collected[0] != "foxX" {
		t.Errorf("Expected foxX, got %v", collected[0])
	}
	if collected[1] != "elttob" {
		t.Errorf("Expected elttob, got %v", collected[1])
	}
}

func TestPublicDriverproxyNotify(t *testing.T) {
	proxy := NewDriverProxyPublic(&AnotherDummyEngine{}, "notifyName")
	proxy.Notify("pub_new_notify", map[string]interface{}{"key": "val"})
	if len(proxy.Engine.Notified) == 0 {
		t.Fatalf("Engine not notified")
	}
	last := proxy.Engine.Notified[len(proxy.Engine.Notified)-1]
	if last.Topic != "pub_new_notify" {
		t.Errorf("Expected topic pub_new_notify, got %v", last.Topic)
	}
	if last.Kw["key"] != "val" {
		t.Errorf("Expected key=val, got %v", last.Kw["key"])
	}
}

func TestPublicDriverproxySetbusyAndIsbusy(t *testing.T) {
	proxy := NewDriverProxyPublic(&AnotherDummyEngine{}, "busy")
	proxy.SetBusy(false)
	if proxy.IsBusy() {
		t.Errorf("isBusy should be false after setBusy(false)")
	}
	proxy.SetBusy(true)
	if !proxy.IsBusy() {
		t.Errorf("isBusy should be true after setBusy(true)")
	}
}

func TestPublicDriverproxySay(t *testing.T) {
	proxy := NewDriverProxyPublic(&AnotherDummyEngine{}, "say")
	proxy.Say("Hi from public!", "pTestName")
	found := false
	for _, q := range proxy.Queue {
		if q.Name == "pTestName" && len(q.Args) > 0 && q.Args[0] == "Hi from public!" {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("Say not queued properly")
	}
}

func TestPublicDriverproxyStop(t *testing.T) {
	proxy := NewDriverProxyPublic(&AnotherDummyEngine{}, "stop")
	proxy.Driver.TimesStopped = 0
	proxy.Stop()
	for len(proxy.Queue) > 0 {
		qf := proxy.Queue[0]
		proxy.Queue = proxy.Queue[1:]
		if qf.Fn != nil {
			qf.Fn()
		}
	}
	if proxy.Driver.TimesStopped != 1 {
		t.Errorf("Expected driver times_stopped=1, got %d", proxy.Driver.TimesStopped)
	}
}