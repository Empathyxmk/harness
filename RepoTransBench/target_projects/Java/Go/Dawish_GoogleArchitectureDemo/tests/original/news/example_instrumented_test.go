package news

import (
	"testing"
)

func TestUseAppContext_GoogleArchitectureNews(t *testing.T) {
	appContextPackageName := "google.architecture.news.test"
	expected := "google.architecture.news.test"
	if appContextPackageName != expected {
		t.Errorf("expected %s, got %s", expected, appContextPackageName)
	}
}