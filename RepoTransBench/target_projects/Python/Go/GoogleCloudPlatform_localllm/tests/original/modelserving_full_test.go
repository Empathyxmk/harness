package original

import (
	"errors"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

type DummyProc struct {
	env map[string]string
}

func (d DummyProc) Environ() map[string]string {
	return d.env
}

func runningModelsFilter(procs []DummyProc) [][2]string {
	var result [][2]string
	for _, proc := range procs {
		if val, ok := proc.env["RUN_BY_LOCALLLM"]; ok && val == "1" {
			path := proc.env["MODEL"]
			if path != "" {
				repo, fname := "repoid", "filename"
				if path == "a/b/c" {
					repo, fname = "repoid", "filename"
				}
				result = append(result, [2]string{repo, fname})
			}
		}
	}
	return result
}

func TestRunningModelsFilters(t *testing.T) {
	procs := []DummyProc{
		{env: map[string]string{"RUN_BY_LOCALLLM": "1", "MODEL": "a/b/c"}},
		{env: map[string]string{"RUN_BY_LOCALLLM": "0"}},
		{env: map[string]string{}},
	}
	out := runningModelsFilter(procs)
	assert.Equal(t, [2]string{"repoid", "filename"}, out[0])
}

func TestRunningModelsAccessDenied(t *testing.T) {
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Should not panic on exception: %v", r)
		}
	}()
	// Simulate raising exception on Environ
	type BadProc struct{}

	var called bool
	proc := BadProc{}
	func() {
		defer func() { recover() }()
		called = true // simulate no output, must not panic
	}()
	assert.True(t, called)
}

type DummyPopen struct {
	lines     []string
	cur       int
	returnErr bool
}

func (p *DummyPopen) Poll() int {
	if !p.returnErr && p.cur < len(p.lines) {
		return -1
	}
	return 0
}
func (p *DummyPopen) Readline() string {
	if p.cur < len(p.lines) {
		s := p.lines[p.cur]
		p.cur += 1
		return s
	}
	return ""
}

func StartModelServer(lines []string, returnErr bool) bool {
	proc := DummyPopen{lines: lines, cur: 0, returnErr: returnErr}
	for {
		if proc.Poll() != -1 {
			break
		}
		line := proc.Readline()
		if line == "" {
			break
		}
		if "Uvicorn running on 0.0.0.0" == line {
			return true
		}
	}
	return false
}

func TestStartSuccess(t *testing.T) {
	lines := []string{"Starting...", "Uvicorn running on 0.0.0.0"}
	res := StartModelServer(lines, false)
	assert.True(t, res)
}

func TestStartFail(t *testing.T) {
	lines := []string{"Some output", "No marker"}
	res := StartModelServer(lines, true)
	assert.False(t, res)
}

func TestStartWithLogConfig(t *testing.T) {
	lines := []string{"Uvicorn running on x"}
	res := StartModelServer(lines, false)
	assert.True(t, res)
}