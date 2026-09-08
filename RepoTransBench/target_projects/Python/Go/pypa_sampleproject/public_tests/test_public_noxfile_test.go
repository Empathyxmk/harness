package public_tests

import (
	"os"
	"strings"
	"testing"
	"go/parser"
	"go/token"
	"go/ast"
	"io/ioutil"
	"path/filepath"
)

func TestLintSessionExistsAndIsDef(t *testing.T) {
	noxfilePath := filepath.Join("..", "noxfile.py")
	src, err := ioutil.ReadFile(noxfilePath)
	if err != nil {
		t.Fatalf("unable to read noxfile: %v", err)
	}

	// As close as possible to: is there a def lint(...) in the file?
	lines := strings.Split(string(src), "\n")
	found := false
	for _, line := range lines {
		if strings.HasPrefix(strings.TrimSpace(line), "def lint(") {
			found = true
			break
		}
	}
	if !found {
		t.Fatalf("lint session must exist as a 'def lint(...' in noxfile.py")
	}
}

func TestLintSessionDecoratorIncludesSession(t *testing.T) {
	noxfilePath := filepath.Join("..", "noxfile.py")
	src, err := ioutil.ReadFile(noxfilePath)
	if err != nil {
		t.Fatalf("unable to read noxfile: %v", err)
	}

	lines := strings.Split(string(src), "\n")
	inLint := false
	foundDecorator := false
	for _, line := range lines {
		l := strings.TrimSpace(line)
		if strings.HasPrefix(l, "def lint(") {
			inLint = true
		} else if inLint {
			break
		} else if strings.HasPrefix(l, "@nox.session") {
			foundDecorator = true
		}
	}
	if !foundDecorator {
		t.Fatalf("lint should be decorated with @nox.session")
	}
}

func TestLintSessionCallsRunWithSpecificArgs(t *testing.T) {
	noxfilePath := filepath.Join("..", "noxfile.py")
	src, err := ioutil.ReadFile(noxfilePath)
	if err != nil {
		t.Fatalf("unable to read noxfile: %v", err)
	}
	words := []string{"flake8", "pytest", "mypy"}
	found := false
	lines := strings.Split(string(src), "\n")
	for _, line := range lines {
		if strings.Contains(line, "session.run") {
			for _, word := range words {
				if strings.Contains(line, word) {
					found = true
					break
				}
			}
		}
	}
	if !found {
		t.Fatalf("Should call session.run with flake8 or pytest or mypy")
	}
}