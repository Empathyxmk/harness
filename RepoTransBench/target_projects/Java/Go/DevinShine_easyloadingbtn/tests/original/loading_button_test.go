package tests

import (
    "testing"
)

type testCallback struct {
    called *bool
}

func (c *testCallback) Complete() {
    *(c.called) = true
}

func createTestLoadingButton() *LoadingButton {
    return NewLoadingButton()
}

func TestLoadingButton_InitialState(t *testing.T) {
    btn := createTestLoadingButton()
    if btn.IsCompleted() {
        t.Errorf("Initial state: expected completed=false, got true")
    }
    if btn.IsShowArc() {
        t.Errorf("Initial state: expected showArc=false, got true")
    }
}

func TestLoadingButton_SetTargetProgress_SetsProgress(t *testing.T) {
    btn := createTestLoadingButton()
    btn.SetTargetProgress(180)
    if btn.GetTargetProgress() != 180 {
        t.Errorf("SetTargetProgress: expected 180, got %d", btn.GetTargetProgress())
    }
}

func TestLoadingButton_SetAndGetCallback(t *testing.T) {
    btn := createTestLoadingButton()
    called := false
    cb := &testCallback{called: &called}
    btn.SetCallback(cb)
    btn.PerformCompleteCallback()
    if !called {
        t.Errorf("Callback was not called")
    }
}

func TestLoadingButton_SetCompleted(t *testing.T) {
    btn := createTestLoadingButton()
    btn.SetCompleted(true)
    if !btn.IsCompleted() {
        t.Errorf("After SetCompleted(true), expected completed=true")
    }
    btn.SetCompleted(false)
    if btn.IsCompleted() {
        t.Errorf("After SetCompleted(false), expected completed=false")
    }
}

func TestLoadingButton_OnClick_WithNotCompleted(t *testing.T) {
    btn := createTestLoadingButton()
    btn.SetCompleted(false)
    btn.PerformClick() // No panic or error expected
    t.Log("PerformClick with not completed: OK (no panic)")
}

func TestLoadingButton_OnClick_WithCompleted(t *testing.T) {
    btn := createTestLoadingButton()
    btn.SetCompleted(true)
    if !btn.IsCompleted() {
        t.Errorf("Expected completed=true before click")
    }
    btn.PerformClick() // Should immediately return; no error expected
    t.Log("PerformClick with completed: OK (no panic)")
}

func TestLoadingButton_SetShowArc(t *testing.T) {
    btn := createTestLoadingButton()
    btn.SetShowArc(true)
    if !btn.IsShowArc() {
        t.Errorf("SetShowArc(true): got false, want true")
    }
    btn.SetShowArc(false)
    if btn.IsShowArc() {
        t.Errorf("SetShowArc(false): got true, want false")
    }
}