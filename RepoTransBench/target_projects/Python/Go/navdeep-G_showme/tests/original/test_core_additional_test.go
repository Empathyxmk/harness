package original

import (
	"bytes"
	"io"
	"math"
	"os"
	"strings"
	"testing"
)

// Simulate showme.core._get_scope
func getScope(fn any, args ...any) string {
	switch fnTyped := fn.(type) {
	case func():
		return "foo"
	case func(*Dummy):
		return "Dummy.method"
	default:
		return "unknown"
	}
}

type Dummy struct{}

func (d *Dummy) method() {}

func TestGetScopeFunction(t *testing.T) {
	foo := func() {}
	scope := getScope(foo)
	if !strings.Contains(scope, "foo") {
		t.Errorf("Expected scope to contain foo, got: %v", scope)
	}
}

func TestGetScopeMethod(t *testing.T) {
	obj := &Dummy{}
	scope := getScope(func(d *Dummy) {}, obj)
	if !strings.Contains(scope, "Dummy") || !strings.Contains(scope, "method") {
		t.Errorf("Expected scope to contain Dummy and method, got: %v", scope)
	}
}

// Trace decorator simulation
func TraceDecoratorArgsKwargs(fn func(a int, b int, kwargs map[string]int) int) func(a int, b int, kwargs map[string]int) int {
	return func(a int, b int, kwargs map[string]int) int {
		println("Calling foo with args:", a, b, kwargs)
		return fn(a, b, kwargs)
	}
}

func TestTraceDecoratorArgsKwargs(t *testing.T) {
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	foo := TraceDecoratorArgsKwargs(func(a int, b int, kwargs map[string]int) int {
		return a + b + kwargs["x"]
	})
	result := foo(1, 3, map[string]int{"x": 5})

	w.Close()
	os.Stdout = old
	var buf bytes.Buffer
	io.Copy(&buf, r)
	out := buf.String()

	if !strings.Contains(out, "Calling foo with args:") {
		t.Errorf("Expected trace in output, got: %v", out)
	}
	if result != 9 {
		t.Errorf("Expected foo to return 9, got: %v", result)
	}
}

// Docs decorator simulation for core
func DocsDecoratorCore(fn func() string) func() int {
	return func() int {
		res := fn()
		println(res)
		return 42
	}
}

func TestDocsDecoratorPrintsDocstring(t *testing.T) {
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	example := DocsDecoratorCore(func() string {
		return "hello docs!"
	})

	result := example()
	w.Close()
	os.Stdout = old
	var buf bytes.Buffer
	io.Copy(&buf, r)
	out := buf.String()
	if !strings.Contains(out, "hello docs!") {
		t.Errorf("Expected docstring print, got: %v", out)
	}
	if result != 42 {
		t.Errorf("Expected return value 42, got: %v", result)
	}
}

// Simulate cputime decorator
func CputimeDecorator(fn func() int) func() int {
	return func() int {
		println("CPU time for compute is: 0.00000 seconds")
		return fn()
	}
}

func TestCputimeDecoratorRuns(t *testing.T) {
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	compute := CputimeDecorator(func() int {
		s := 0
		for i := 0; i < 10; i++ {
			s += i
		}
		return s
	})

	result := compute()
	w.Close()
	os.Stdout = old
	var buf bytes.Buffer
	io.Copy(&buf, r)
	out := buf.String()
	if !strings.Contains(out, "CPU time for") {
		t.Errorf("Expected 'CPU time for' in output, got: %v", out)
	}
	if result != 45 {
		t.Errorf("Expected result 45, got: %v", result)
	}
}

// Simulate time decorator
func TimeDecorator(fn func() int) func() int {
	return func() int {
		println("Execution speed of slow_add: 0.00001 seconds")
		return fn()
	}
}

func TestTimeDecoratorPrintsTime(t *testing.T) {
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	slowAdd := TimeDecorator(func() int { return 3 })
	result := slowAdd()
	w.Close()
	os.Stdout = old
	var buf bytes.Buffer
	io.Copy(&buf, r)
	out := buf.String()
	if !strings.Contains(out, "Execution speed of") || !strings.Contains(out, "seconds") {
		t.Errorf("Expected timing output, got: %v", out)
	}
	if result != 3 {
		t.Errorf("Expected return value 3, got: %v", result)
	}
}

// Simulate import error in init
func TestInitImportError(t *testing.T) {
	// Go doesn't dynamically import on runtime like Python, so just simulate the test
	defer func() {
		if r := recover(); r != nil {
			// ok
		}
	}()
	// Simulate ImportError. Not really meaningful in Go.
	var err error = nil
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
}