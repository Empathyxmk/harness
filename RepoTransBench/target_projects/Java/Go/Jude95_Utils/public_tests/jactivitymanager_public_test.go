package public_tests

import (
	"sync"
	"testing"
)

type DummyActivity struct {
	Name string
}

type activityStackType struct {
	stack []*DummyActivity
	mu    sync.Mutex
}

var activityStack = &activityStackType{}

func (a *activityStackType) Clear() {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.stack = nil
}

func (a *activityStackType) Push(act *DummyActivity) {
	a.mu.Lock()
	defer a.mu.Unlock()
	a.stack = append(a.stack, act)
}

func (a *activityStackType) Remove(act *DummyActivity) {
	a.mu.Lock()
	defer a.mu.Unlock()
	res := []*DummyActivity{}
	for _, e := range a.stack {
		if e != act {
			res = append(res, e)
		}
	}
	a.stack = res
}

func (a *activityStackType) Top() *DummyActivity {
	a.mu.Lock()
	defer a.mu.Unlock()
	if len(a.stack) == 0 {
		return nil
	}
	return a.stack[len(a.stack)-1]
}

func (a *activityStackType) All() []*DummyActivity {
	a.mu.Lock()
	defer a.mu.Unlock()
	return append([]*DummyActivity(nil), a.stack...)
}

func currentActivity() *DummyActivity {
	return activityStack.Top()
}

func closeActivity(act *DummyActivity) {
	if act == nil {
		return
	}
	activityStack.Remove(act)
}
func closeAllActivity() {
	activityStack.Clear()
}
func closeActivityByName(name string) {
	activityStack.mu.Lock()
	defer activityStack.mu.Unlock()
	acts := []*DummyActivity{}
	for _, act := range activityStack.stack {
		if act.Name != name && ("com.jude.utils."+act.Name) != name {
			acts = append(acts, act)
		}
	}
	activityStack.stack = acts
}
func getCurrentActivityName() string {
	act := currentActivity()
	if act == nil {
		return ""
	}
	return "com.jude.utils." + act.Name
}
func getActivityStack() []*DummyActivity {
	return activityStack.All()
}

func TestStackAdditionAndRetrievalPublic(t *testing.T) {
	a1 := &DummyActivity{"FirstActivity"}
	a2 := &DummyActivity{"SecondActivity"}

	activityStack.Clear()
	if currentActivity() != nil {
		t.Errorf("Expected nil")
	}
	activityStack.Push(a1)
	if currentActivity() != a1 {
		t.Errorf("Should be a1")
	}
	activityStack.Push(a2)
	if currentActivity() != a2 {
		t.Errorf("Should be a2")
	}
	closeActivity(a1)
	if currentActivity() != a2 {
		t.Errorf("Should be a2 after closing a1")
	}
	closeActivity(a2)
	if currentActivity() != nil {
		t.Errorf("Should be nil after closing a2")
	}
}

func TestCloseActivityPublic(t *testing.T) {
	a1 := &DummyActivity{"FirstActivity"}
	a2 := &DummyActivity{"SecondActivity"}
	activityStack.Clear()
	activityStack.Push(a1)
	activityStack.Push(a2)
	closeActivity(a1)
	if currentActivity() != a2 {
		t.Errorf("Should be a2")
	}
	closeActivity(nil)
	if currentActivity() != a2 {
		t.Errorf("Should still be a2 after closing nil")
	}
}

func TestCloseAllActivityPublic(t *testing.T) {
	a1 := &DummyActivity{"XActivity"}
	a2 := &DummyActivity{"YActivity"}
	activityStack.Clear()
	activityStack.Push(a1)
	activityStack.Push(a2)
	closeAllActivity()
	if currentActivity() != nil {
		t.Errorf("After closing all, should be nil")
	}
}

func TestCloseActivityByNamePublic(t *testing.T) {
	a1 := &DummyActivity{"TestA"}
	a2 := &DummyActivity{"TestB"}
	activityStack.Clear()
	activityStack.Push(a1)
	activityStack.Push(a2)
	closeActivityByName("com.jude.utils.TestA")
	if currentActivity() != a2 {
		t.Errorf("Should be a2 after close by name TestA")
	}
}

func TestGetCurrentActivityNamePublic(t *testing.T) {
	a1 := &DummyActivity{"LandingScreen"}
	activityStack.Clear()
	activityStack.Push(a1)
	if getCurrentActivityName() != "com.jude.utils.LandingScreen" {
		t.Errorf("Should be LandingScreen")
	}
	closeActivity(a1)
	if getCurrentActivityName() != "" {
		t.Errorf("Should be blank after closing activity")
	}
}

func TestGetActivityStackPublic(t *testing.T) {
	a1 := &DummyActivity{"SomeActivity"}
	a2 := &DummyActivity{"AnotherActivity"}
	activityStack.Clear()
	activityStack.Push(a1)
	activityStack.Push(a2)
	stack1 := getActivityStack()
	if len(stack1) == 0 {
		t.Errorf("Should not be empty")
	}
	stack2 := getActivityStack()
	if len(stack1) != len(stack2) {
		t.Errorf("Stack lengths should match")
	}
}