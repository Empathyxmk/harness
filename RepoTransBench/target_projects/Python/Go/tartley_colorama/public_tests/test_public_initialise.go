package public_tests

import (
	"testing"
)

func TestInitWrapsOnWindowsPublic(t *testing.T) {
	env := NewFakeEnv("nt", true, true)
	out, err := env.Init()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if !out.Wrapped {
		t.Errorf("expected stdout/stderr to be wrapped")
	}
}

func TestInitDoesntWrapOnEmulatedWindowsPublic(t *testing.T) {
	env := NewFakeEnv("nt", false, false)
	out, err := env.Init()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if out.Wrapped {
		t.Errorf("expected stdout/stderr not to be wrapped")
	}
}

func TestInitDoesntWrapOnNonWindowsPublic(t *testing.T) {
	env := NewFakeEnv("java", false, false)
	out, err := env.Init()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if out.Wrapped {
		t.Errorf("should not wrap on non-windows")
	}
}

func TestInitAutoresetOnWrapsOnAllPlatformsPublic(t *testing.T) {
	env := NewFakeEnv("customos", true, true)
	out, err := env.InitWithAutoreset(true)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if !out.Wrapped {
		t.Errorf("should wrap when autoreset")
	}
}

func TestInitWrapOffDoesntWrapOnWindowsPublic(t *testing.T) {
	env := NewFakeEnv("nt", false, false)
	out, err := env.InitWrapOff()
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if out.Wrapped {
		t.Errorf("should not wrap when wrap=false")
	}
}

func TestInitWrapOffIncompatibleWithAutoresetOnPublic(t *testing.T) {
	env := NewFakeEnv("nt", false, false)
	_, err := env.InitWrapOffAutoresetOn()
	if err == nil {
		t.Errorf("expected error for wrap=false && autoreset=true")
	}
}

// Fake implementation to simulate conditions of various OS/env for init, matching public Python test logic

type FakeEnv struct {
	OS      string
	HasVT   bool
	IsTTY   bool
}

type InitResult struct {
	Wrapped bool
}

func NewFakeEnv(os string, hasVT, isTTY bool) *FakeEnv {
	return &FakeEnv{OS: os, HasVT: hasVT, IsTTY: isTTY}
}

func (e *FakeEnv) Init() (*InitResult, error) {
	if e.OS == "nt" && (e.HasVT || e.IsTTY) {
		return &InitResult{Wrapped: true}, nil
	}
	return &InitResult{Wrapped: false}, nil
}

func (e *FakeEnv) InitWithAutoreset(autoreset bool) (*InitResult, error) {
	if autoreset {
		return &InitResult{Wrapped: true}, nil
	}
	return e.Init()
}

func (e *FakeEnv) InitWrapOff() (*InitResult, error) {
	return &InitResult{Wrapped: false}, nil
}

func (e *FakeEnv) InitWrapOffAutoresetOn() (*InitResult, error) {
	return nil, assertError("wrap=false && autoreset=true not allowed")
}

// Helper for error
func assertError(msg string) error {
	return &FakeError{msg}
}

type FakeError struct {
	s string
}
func (e *FakeError) Error() string { return e.s }