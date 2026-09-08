package original

import "testing"

// Simulate WebView and EditText
type WebView struct {
	JS      bool
	URL     string
}

type EditText struct {
	text string
}

type InputValidation2URISchemeActivity struct {
	wview *WebView
	uri   *EditText
}

func NewInputValidation2URISchemeActivity() *InputValidation2URISchemeActivity {
	return &InputValidation2URISchemeActivity{
		wview: &WebView{JS: true},
		uri:   &EditText{},
	}
}

func (a *InputValidation2URISchemeActivity) GetViewById(id int) (webview *WebView, edittext *EditText) {
	return a.wview, a.uri
}

// Realistically only implements needed functionality for testing
func (a *InputValidation2URISchemeActivity) Get(_ interface{}) {
	a.wview.URL = a.uri.text
}

func TestInputValidation2URI_onCreate_setsLayoutAndJS(t *testing.T) {
	act := NewInputValidation2URISchemeActivity()
	webview, _ := act.GetViewById(1)
	if webview == nil {
		t.Fatal("Expected WebView not nil")
	}
	if !webview.JS {
		t.Error("Expected JavaScript to be enabled")
	}
}

func TestInputValidation2URI_get_loadsUrlFromEditText(t *testing.T) {
	act := NewInputValidation2URISchemeActivity()
	_, edittext := act.GetViewById(1)
	webview, _ := act.GetViewById(1)

	edittext.text = "https://payatu.com/"
	act.uri = edittext

	act.Get(nil)

	if webview.URL != "https://payatu.com/" {
		t.Errorf("Expected WebView URL to be %q, got %q", "https://payatu.com/", webview.URL)
	}
}