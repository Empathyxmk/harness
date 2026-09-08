// Code generated from src/latexify/test_utils.py
package original

import (
	"go/ast"
	"go/token"
	"reflect"
	"runtime"
	"testing"
)

// requireAtLeast returns a function decorator that skips test if GoMinor < minor.
// In Go, we return a boolean to check in the test.
func requireAtLeast(minor int) func(*testing.T) bool {
	return func(t *testing.T) bool {
		ver := runtime.Version()
		// Go version: go1.x[.y...]
		var vmin int
		fmtSScanned, _ := fmt.Sscanf(ver, "go1.%d", &vmin)
		if fmtSScanned == 1 && vmin < minor {
			t.Skipf("Go minor version < %d", minor)
			return false
		}
		return true
	}
}

// requireAtMost returns a function decorator that skips test if GoMinor > minor.
func requireAtMost(minor int) func(*testing.T) bool {
	return func(t *testing.T) bool {
		ver := runtime.Version()
		var vmin int
		fmtSScanned, _ := fmt.Sscanf(ver, "go1.%d", &vmin)
		if fmtSScanned == 1 && vmin > minor {
			t.Skipf("Go minor version > %d", minor)
			return false
		}
		return true
	}
}

// astEqual checks deep equality of two ASTs, ignoring Pos info and End info as per logic in original.
func astEqual(observed, expected ast.Node) bool {
	return astEqualCustom(observed, expected, map[string]struct{}{
		"Pos": {}, "End": {},
	})
}

func astEqualCustom(observed, expected ast.Node, ignore map[string]struct{}) bool {
	if reflect.TypeOf(observed) != reflect.TypeOf(expected) {
		return false
	}

	if observed == nil || expected == nil {
		return observed == expected
	}
	rvObs := reflect.ValueOf(observed)
	rvExp := reflect.ValueOf(expected)
	if rvObs.Kind() == reflect.Ptr {
		rvObs = rvObs.Elem()
	}
	if rvExp.Kind() == reflect.Ptr {
		rvExp = rvExp.Elem()
	}
	if !rvObs.IsValid() || !rvExp.IsValid() {
		return rvObs.IsValid() == rvExp.IsValid()
	}
	for i := 0; i < rvObs.NumField(); i++ {
		name := rvObs.Type().Field(i).Name
		// ignore position, End, other specified keys
		if _, ok := ignore[name]; ok {
			continue
		}
		fObs := rvObs.Field(i)
		fExp := rvExp.Field(i)

		switch fObs.Kind() {
		case reflect.Ptr, reflect.Interface:
			if !astEqualCustom(fObs.Interface().(ast.Node), fExp.Interface().(ast.Node), ignore) {
				return false
			}
		case reflect.Slice:
			if fObs.Len() != fExp.Len() {
				return false
			}
			for j := 0; j < fObs.Len(); j++ {
				// go/ast fields can be []ast.Node or []*ast.Thing
				// Must deal with interface conversion
				if fObs.Index(j).Kind() == reflect.Interface || fObs.Index(j).Kind() == reflect.Ptr || fObs.Index(j).Kind() == reflect.Struct {
					if !astEqualCustom(fObs.Index(j).Interface().(ast.Node), fExp.Index(j).Interface().(ast.Node), ignore) {
						return false
					}
				} else if !reflect.DeepEqual(fObs.Index(j).Interface(), fExp.Index(j).Interface()) {
					return false
				}
			}
		default:
			if !reflect.DeepEqual(fObs.Interface(), fExp.Interface()) {
				return false
			}
		}
	}
	return true
}

// assertAstEqual calls t.Fatalf if the ASTs are not equal (ignoring Pos/End).
func assertAstEqual(t *testing.T, observed, expected ast.Node) {
	if !astEqual(observed, expected) {
		t.Fatalf("AST does not match.\n observed=%#v\n expected=%#v\n", observed, expected)
	}
}