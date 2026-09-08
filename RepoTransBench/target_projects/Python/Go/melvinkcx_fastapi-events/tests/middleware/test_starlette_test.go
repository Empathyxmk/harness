package middleware

import (
	"testing"
)

func TestStarletteMiddlewareBasic(t *testing.T) {
	app := NewFakeStarletteApp()
	req := "fakeRequest"
	resp := app.ProcessRequest(req)
	want := "starlette middleware processed: fakeRequest"
	if resp != want {
		t.Errorf("starlette middleware: got %q, want %q", resp, want)
	}
}

type FakeStarletteApp struct{}

func NewFakeStarletteApp() *FakeStarletteApp { return &FakeStarletteApp{} }
func (f *FakeStarletteApp) ProcessRequest(req string) string {
	return "starlette middleware processed: " + req
}