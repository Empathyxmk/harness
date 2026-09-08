package middleware

import (
	"testing"
)

func TestStarliteMiddlewareBasic(t *testing.T) {
	app := NewFakeStarliteApp()
	req := "anotherFakeRequest"
	resp := app.ProcessRequest(req)
	want := "starlite middleware processed: anotherFakeRequest"
	if resp != want {
		t.Errorf("starlite middleware: got %q, want %q", resp, want)
	}
}

type FakeStarliteApp struct{}

func NewFakeStarliteApp() *FakeStarliteApp { return &FakeStarliteApp{} }
func (f *FakeStarliteApp) ProcessRequest(req string) string {
	return "starlite middleware processed: " + req
}