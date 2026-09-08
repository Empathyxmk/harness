package original

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
	// Remove by pointer
	result := []*DummyActivity{}
	for _, e := range a.stack {
		if e != act {
			result = append(result, e)
		}
	}
	a.stack = result
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

// JActivityManager emulation
func currentActivity() *DummyActivity {
	return activityStack.Top()
}
func closeActivity(act *DummyActivity) {
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

// -- TESTS -------------------------------

func TestStackAdditionAndRetrieval(t *testing.T) {
	a1 := &DummyActivity{"A1"}
	a2 := &DummyActivity{"A2"}

	activityStack.Clear()
	if currentActivity() != nil {
		t.Errorf("Expected nil top activity.")
	}
	activityStack.Push(a1)
	if currentActivity() != a1 {
		t.Errorf("Top activity not a1.")
	}
	activityStack.Push(a2)
	if currentActivity() != a2 {
		t.Errorf("Top activity not a2.")
	}
	closeActivity(a1)
	if currentActivity() != a2 {
		t.Errorf("Top activity after closing a1 should be a2.")
	}
	closeActivity(a2)
	if currentActivity() != nil {
		t.Errorf("Top activity after closing all should be nil.")
	}
}

func TestCloseActivity(t *testing.T) {
	a1 := &DummyActivity{"A1"}
	a2 := &DummyActivity{"A2"}
	activityStack.Clear()
	activityStack.Push(a1)
	activityStack.Push(a2)
	closeActivity(a2)
	if currentActivity() != a1 {
		t.Errorf("Expected top to be a1")
	}
	closeActivity(nil)
	if currentActivity() != a1 {
		t.Errorf("Closing nil should not change state")
	}
}

func TestCloseAllActivity(t *testing.T) {
	a1 := &DummyActivity{"A1"}
	a2 := &DummyActivity{"A2"}
	activityStack.Clear()
	activityStack.Push(a1)
	activityStack.Push(a2)
	closeAllActivity()
	if currentActivity() != nil {
		t.Errorf("Expected stack empty after closeAllActivity")
	}
}

func TestCloseActivityByName(t *testing.T) {
	a1 := &DummyActivity{"ActivityA"}
	a2 := &DummyActivity{"ActivityB"}
	activityStack.Clear()
	activityStack.Push(a1)
	activityStack.Push(a2)
	closeActivityByName("com.jude.utils.ActivityB")
	if currentActivity() != a1 {
		t.Errorf("Expected top to be a1 after closing ActivityB")
	}
}

func TestGetCurrentActivityName(t *testing.T) {
	a1 := &DummyActivity{"MainScreen"}
	activityStack.Clear()
	activityStack.Push(a1)
	if getCurrentActivityName() != "com.jude.utils.MainScreen" {
		t.Errorf("Expected MainScreen")
	}
	closeActivity(a1)
	if getCurrentActivityName() != "" {
		t.Errorf("Expected empty after removing activity")
	}
}

func TestGetActivityStack(t *testing.T) {
	a1 := &DummyActivity{"AA"}
	activityStack.Clear()
	activityStack.Push(a1)
	stack1 := getActivityStack()
	if len(stack1) == 0 {
		t.Errorf("Expected non-empty stack")
	}
	stack2 := getActivityStack()
	if len(stack1) != len(stack2) {
		t.Errorf("Stack size mismatch")
	}
}