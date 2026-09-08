package original

import (
	"strings"
	"testing"

	"stephenmcd_django_forms_builder/formsbuilder"
)

func TestIsFileExtensions(t *testing.T) {
	if !formsbuilder.IsFile("photo.PNG") {
		t.Errorf("photo.PNG should be recognized as file")
	}
	if !formsbuilder.IsFile("document.PDF") {
		t.Errorf("document.PDF should be recognized as file")
	}
	if formsbuilder.IsFile("example.txt") {
		t.Errorf("example.txt should not be a file")
	}
	if formsbuilder.IsFile("no_dot") {
		t.Errorf("no_dot should not be a file")
	}
}

func TestSlugifyBasic(t *testing.T) {
	s := " Hello__World__ "
	sl := formsbuilder.Slugify(s)
	if sl != "hello-world" {
		t.Errorf("expected slug 'hello-world', got '%s'", sl)
	}
}

func TestIsEmailCases(t *testing.T) {
	if !formsbuilder.IsEmail("foo@bar.com") {
		t.Error("foo@bar.com should be recognized as email")
	}
	if formsbuilder.IsEmail("notanemail") {
		t.Error("notanemail should not be recognized as email")
	}
	if formsbuilder.IsEmail("@nodomain") {
		t.Error("@nodomain should not be recognized as email")
	}
}

func TestContentAsTxtHtml(t *testing.T) {
	text := formsbuilder.ContentAsText(123)
	html := formsbuilder.ContentAsHTML(struct{}{})
	if !strings.Contains(text, "text") {
		t.Error("ContentAsText should contain 'text'")
	}
	if !strings.Contains(html, "html") {
		t.Error("ContentAsHTML should contain 'html'")
	}
}

func TestGetAdminUrlFormat(t *testing.T) {
	url := formsbuilder.GetAdminURL(nil)
	if !(strings.Contains(url, "myapp/dummy/1")) {
		t.Errorf("expected url to contain myapp/dummy/1, got %s", url)
	}
}