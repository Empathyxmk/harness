package public_tests

import (
    "testing"
)

type testCallbackPublic struct {
    called *bool
}

func (c *testCallbackPublic) Complete() {
    *(c.called) = true
}

func createTestLoadingButtonPublic() *LoadingButton {
    return NewLoadingButton()
}

func TestLoadingButton_InitialState_PublicVariant(t *testing.T) {
    btn := createTestLoadingButtonPublic()
    if btn.IsCompleted() {
        t.Errorf("Initial state (public): expected completed=false, got true")
    }
    if btn.IsShowArc() {
        t.Errorf("Initial state (public): expected showArc=false, got true")
    }
}

func TestLoadingButton_SetTargetProgress_SetsDifferentProgress(t *testing.T) {
    btn := createTestLoadingButtonPublic()
    btn.SetTargetProgress(250)
    if btn.GetTargetProgress() != 250 {
        t.Errorf("SetTargetProgress: expected 250, got %d", btn.GetTargetProgress())
    }
}

func TestLoadingButton_SetAndGetCallback_Public(t *testing.T) {
    btn := createTestLoadingButtonPublic()
    called := false
    cb := &testCallbackPublic{called: &called}
    btn.SetCallback(cb)
    btn.PerformCompleteCallback()
    if !called {
        t.Errorf("Callback (public) was not called")
    }
}

func TestLoadingButton_SetCompleted_AlternatePattern(t *testing.T) {
    btn := createTestLoadingButtonPublic()
    btn.SetCompleted(false)
    if btn.IsCompleted() {
        t.Errorf("After SetCompleted(false), expected completed=false")
    }
    btn.SetCompleted(true)
    if !btn.IsCompleted() {
        t.Errorf("After SetCompleted(true), expected completed=true")
    }
}

func TestLoadingButton_OnClick_WithCompleted_Public(t *testing.T) {
    btn := createTestLoadingButtonPublic()
    btn.SetCompleted(true)
    if !btn.IsCompleted() {
        t.Errorf("Expected completed=true before click (public)")
    }
    btn.PerformClick() // Should return immediately, no error
    t.Log("PerformClick(public) with completed: OK (no panic)")
}

func TestLoadingButton_OnClick_WithNotCompleted_Public(t *testing.T) {
    btn := createTestLoadingButtonPublic()
    btn.SetCompleted(false)
    btn.PerformClick()
    t.Log("PerformClick(public) with not completed: OK (no panic)")
}

func TestLoadingButton_SetShowArc_Public(t *testing.T) {
    btn := createTestLoadingButtonPublic()
    btn.SetShowArc(false)
    if btn.IsShowArc() {
        t.Errorf("SetShowArc(false): got true, want false")
    }
    btn.SetShowArc(true)
    if !btn.IsShowArc() {
        t.Errorf("SetShowArc(true): got false, want true")
    }
}