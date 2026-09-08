package sample

import (
	"testing"
)

// WebHandler acts as router/fallback for web URLs; our Go mock is minimal for the tests.
type Context struct {
	activityStarted bool
	startedIntent   *Intent
}
type Intent struct {
	Url   string
	Flags int
	Bund  map[string]interface{}
}
type WebHandler struct{}

func (w *WebHandler) OnTargetNotFound(ctx *Context, uri string, extras map[string]interface{}, flags *int) bool {
	if uri[:4] == "http" || uri[:5] == "https" {
		intent := &Intent{Url: uri, Bund: extras}
		if flags != nil {
			intent.Flags = *flags
		}
		ctx.activityStarted = true
		ctx.startedIntent = intent
		return true
	}
	return false
}

func TestOnTargetNotFound_webScheme_withoutFlags(t *testing.T) {
	ctx := &Context{}
	handler := &WebHandler{}
	webUri := "https://example.com"
	result := handler.OnTargetNotFound(ctx, webUri, map[string]interface{}{}, nil)
	if !result {
		t.Error("Should return true for web URLs")
	}
	if !ctx.activityStarted {
		t.Error("startActivity should have been called")
	}
}

func TestOnTargetNotFound_webScheme_withFlags(t *testing.T) {
	ctx := &Context{}
	handler := &WebHandler{}
	webUri := "https://example.com"
	flags := 8192 // simulate FLAG_ACTIVITY_NEW_TASK
	extras := map[string]interface{}{}
	result := handler.OnTargetNotFound(ctx, webUri, extras, &flags)
	if !result {
		t.Error("Should return true for web URLs")
	}
	if ctx.startedIntent == nil || ctx.startedIntent.Url != webUri {
		t.Error("Intent URL not set correctly")
	}
	if ctx.startedIntent.Flags != 8192 {
		t.Errorf("Intent flags not set: got %v, want %v", ctx.startedIntent.Flags, 8192)
	}
}

func TestOnTargetNotFound_nonWebScheme(t *testing.T) {
	ctx := &Context{}
	handler := &WebHandler{}
	nonWebUri := "foo://bar"
	result := handler.OnTargetNotFound(ctx, nonWebUri, map[string]interface{}{}, nil)
	if result {
		t.Error("Should return false for non-web scheme")
	}
	if ctx.activityStarted {
		t.Error("Should not have started activity")
	}
}