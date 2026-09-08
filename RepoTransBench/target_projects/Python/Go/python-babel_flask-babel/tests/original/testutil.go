package original

import "testing"

// Shared helpers for context simulation.
type TestApp struct {
	Config map[string]interface{}
}

func withTestRequestContext(app *TestApp, fn func()) {
	// Simulated request context for test
	fn()
}

func withAppContext(app *TestApp, fn func()) {
	// Simulated app context for test
	fn()
}