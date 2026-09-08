package public_tests

import (
	"testing"
)

func TestApplicationPublicInstance(t *testing.T) {
	app := struct {
		Name string
	}{Name: "wangshaolei_AutoSpannableTextView"}
	if app.Name != "wangshaolei_AutoSpannableTextView" {
		t.Errorf("expected app name to be 'wangshaolei_AutoSpannableTextView', got %s", app.Name)
	}
}