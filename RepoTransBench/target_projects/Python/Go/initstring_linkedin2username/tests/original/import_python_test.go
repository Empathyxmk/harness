package original

import (
	"os"
	"testing"
)

func TestBasicImports(t *testing.T) {
	_ = os.Args // using "os" import
	_ = t // using the stdlib
	t.Log("This test verifies the ability to import os and stdlib packages in Go. (Coverage/pytest not relevant for Go tests.)")
}