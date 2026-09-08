// Code generated from public_tests/test_public_utils.py
package public_tests

import (
	"testing"
	"go/ast"
	"runtime"
	"strings"
	"github.com/yourusername/googlelatexify/tests/original"
)

func TestRequireAtLeastDecorator(t *testing.T) {
	called := struct{ Value bool }{false}
	f := func() {
		called.Value = true
	}
	fn := func() {
		f()
	}
	// Equivalent to @require_at_least(0) in Go: always true
	if !original.RequireAtLeast(0)(t) {
		t.Fatal("requireAtLeast(0) should not skip")
	}
	fn()
	if !called.Value {
		t.Error("function was not called")
	}
	// Should not call if minor > sys.version_info.minor
	called2 := struct{ Value bool }{false}
	f2 := func() { called2.Value = true }
	currentMinor := goMinor()
	blocked := original.RequireAtLeast(currentMinor+1)
	if blocked(t) {
		f2()
	}
	if called2.Value {
		t.Error("should not have been called")
	}
}

func TestRequireAtMostDecorator(t *testing.T) {
	called := struct{ Value bool }{false}
	f := func() { called.Value = true }
	if !original.RequireAtMost(100)(t) {
		f()
	}
	if !called.Value {
		t.Error("should call as version is below 100")
	}
	called2 := struct{ Value bool }{false}
	blocked := original.RequireAtMost(goMinor()-1)
	if blocked(t) {
		called2.Value = true
	}
	if called2.Value {
		t.Error("should not have been called")
	}
}

func TestAstEqualAndAssertAstEqualSimple(t *testing.T) {
	src := "b := 3"
	file := parseStmtFile(src)
	expected := parseStmtFile(src)
	if !original.AstEqual(file, expected) {
		t.Error("AST should be equal")
	}
	original.AssertAstEqual(t, file, expected)
}

func TestAstEqualAndAssertAstEqualExpr(t *testing.T) {
	src := "x + 2"
	file := parseExprFile(src)
	expected := parseExprFile(src)
	if !original.AstEqual(file, expected) {
		t.Error("AST should be equal")
	}
	original.AssertAstEqual(t, file, expected)
}

// Helper to get the Go minor version
func goMinor() int {
	ver := runtime.Version()
	vmin := 0
	fmtSScanned, _ := fmt.Sscanf(ver, "go1.%d", &vmin)
	if fmtSScanned == 1 {
		return vmin
	}
	return 0
}

// Helper to parse Go code as *ast.File
func parseStmtFile(src string) *ast.File {
	fset := token.NewFileSet()
	f, err := parser.ParseFile(fset, "", "package main\n"+src, parser.AllErrors)
	if err != nil {
		panic(err)
	}
	return f
}

func parseExprFile(src string) ast.Expr {
	fset := token.NewFileSet()
	e, err := parser.ParseExpr(src)
	if err != nil {
		panic(err)
	}
	return e
}