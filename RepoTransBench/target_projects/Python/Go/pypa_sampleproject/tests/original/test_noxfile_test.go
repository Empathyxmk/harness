package original

import (
	"errors"
	"testing"
)

type DummySession struct {
	Installed [][]string
	Runs      [][]string
	Posargs   []string
}

func (s *DummySession) Install(args ...string) {
	s.Installed = append(s.Installed, args)
}

func (s *DummySession) Run(args ...string) {
	s.Runs = append(s.Runs, args)
}

// Lint simulates noxfile lint session
func Lint(session *DummySession) {
	session.Install("flake8")
	session.Run("flake8")
}

// BuildAndCheckDists simulates build+check session
func BuildAndCheckDists(session *DummySession) {
	session.Install("wheel")
	session.Run("python", "setup.py", "sdist", "bdist_wheel")
}

// Tests simulates tests session
func Tests(session *DummySession, buildAndCheck func(*DummySession), listDir func(string) []string, pathJoin func(string, string) string) {
	buildAndCheck(session)
	files := listDir(".")
	for _, file := range files {
		_ = pathJoin("dist", file)
	}
}

func TestLintRunsAndInstalls(t *testing.T) {
	s := &DummySession{}
	Lint(s)
	foundInstall := false
	foundRun := false
	for _, targs := range s.Installed {
		for _, a := range targs {
			if a == "flake8" {
				foundInstall = true
			}
		}
	}
	for _, targs := range s.Runs {
		for _, a := range targs {
			if a == "flake8" {
				foundRun = true
			}
		}
	}
	if !foundInstall {
		t.Error("flake8 not installed")
	}
	if !foundRun {
		t.Error("flake8 not run")
	}
}

func TestBuildAndCheckDistsInvocations(t *testing.T) {
	s := &DummySession{}
	BuildAndCheckDists(s)
	if len(s.Installed) == 0 {
		t.Error("Expected installs")
	}
	if len(s.Runs) == 0 {
		t.Error("Expected runs")
	}
}

func TestTestsInvokesBuild(t *testing.T) {
	s := &DummySession{}
	buildAndCheck := func(sess *DummySession) {
		sess.Run("build_and_check_called")
	}
	listDir := func(_ string) []string {
		return []string{"wheel.whl", "source.tar.gz"}
	}
	pathJoin := func(a, b string) string {
		return a + "/" + b
	}
	Tests(s, buildAndCheck, listDir, pathJoin)
	found := false
	for _, targs := range s.Runs {
		for _, a := range targs {
			if a == "build_and_check_called" {
				found = true
			}
		}
	}
	if !found {
		t.Error("tests did not invoke build_and_check_dists")
	}
}