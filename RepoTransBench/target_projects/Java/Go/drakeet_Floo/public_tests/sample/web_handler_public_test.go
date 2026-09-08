package sample

import (
	"testing"
)

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
	if len(uri) >= 4 && (uri[:4] == "http") {
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

func TestOnTargetNotFound_webScheme_withoutFlags_public(t *testing.T) {
	ctx := &Context{}
	handler := &WebHandler{}
	webUri := "http://public-example.org"
	result := handler.OnTargetNotFound(ctx, webUri, map[string]interface{}{}, nil)
	if !result {
		t.Error("Should return true for web URLs")
	}
	if !ctx.activityStarted {
		t.Error("startActivity should have been called")
	}
}

func TestOnTargetNotFound_webScheme_withFlags_public(t *testing.T) {
	ctx := &Context{}
	handler := &WebHandler{}
	webUri := "http://public-example.org"
	flags := 131072 // simulate FLAG_ACTIVITY_REORDER_TO_FRONT (arbitrary)
	extras := map[string]interface{}{}
	result := handler.OnTargetNotFound(ctx, webUri, extras, &flags)
	if !result {
		t.Error("Should return true for web URLs")
	}
	if ctx.startedIntent == nil || ctx.startedIntent.Url != webUri {
		t.Error("Intent URL not set correctly")
	}
	if ctx.startedIntent.Flags != 131072 {
		t.Errorf("Intent flags not set: got %v, want %v", ctx.startedIntent.Flags, 131072)
	}
}

func TestOnTargetNotFound_nonWebScheme_public(t *testing.T) {
	ctx := &Context{}
	handler := &WebHandler{}
	nonWebUri := "customscheme://baz"
	result := handler.OnTargetNotFound(ctx, nonWebUri, map[string]interface{}{}, nil)
	if result {
		t.Error("Should return false for non-web scheme")
	}
	if ctx.activityStarted {
		t.Error("Should not have started activity")
	}
}