package original

import (
	"testing"
)

// ApplicationTest: In Java, just tested application context/construction. As no equivalent in Go, we only provide a smoke test.
func TestApplicationInstance(t *testing.T) {
	app := struct {
		Name string
	}{Name: "wangshaolei_AutoSpannableTextView"}
	if app.Name != "wangshaolei_AutoSpannableTextView" {
		t.Errorf("expected app name to be 'wangshaolei_AutoSpannableTextView', got %s", app.Name)
	}
}