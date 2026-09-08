// Code generated from public_tests/test_public_ast_utils.py
package public_tests

import (
	"go/ast"
	"testing"
)

// Dummy implementation for public AST utility tests
func TestPublicAstBodyToExpr(t *testing.T) {
	node := &ast.AssignStmt{
		Lhs: []ast.Expr{&ast.Ident{Name: "y"}},
		Tok: token.DEFINE,
		Rhs: []ast.Expr{&ast.BasicLit{Kind: token.INT, Value: "12"}},
	}
	// BodyToExpr would be implemented as in your codebase (not shown here)
}

func TestPublicAstIsSimpleReturn(t *testing.T) {
	fnNode := &ast.FuncDecl{
		Name: &ast.Ident{Name: "f"},
		Type: &ast.FuncType{},
		Body: &ast.BlockStmt{
			List: []ast.Stmt{&ast.ReturnStmt{Results: []ast.Expr{&ast.BasicLit{Kind: token.STRING, Value: "\"abc\""}}}},
		},
	}
	fn2Node := &ast.FuncDecl{
		Name: &ast.Ident{Name: "g"},
		Type: &ast.FuncType{},
		Body: &ast.BlockStmt{
			List: []ast.Stmt{
				&ast.AssignStmt{Lhs: []ast.Expr{&ast.Ident{Name: "x"}}, Tok: token.DEFINE, Rhs: []ast.Expr{&ast.BasicLit{Kind: token.INT, Value: "3"}}},
				&ast.ReturnStmt{Results: []ast.Expr{&ast.Ident{Name: "x"}}},
			},
		},
	}
	if !IsSimpleReturn(fnNode) {
		t.Error("Should be simple return")
	}
	if IsSimpleReturn(fn2Node) {
		t.Error("Should not be simple return")
	}
}

// ...Continue implementing the rest of public AST util tests with proper Go AST logic.