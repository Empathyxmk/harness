package public_tests

import (
	"testing"

	"editorconfig"
)

type FakeOutPair struct {
	key string
	val string
}

func (f FakeOutPair) GetKey() string { return f.key }
func (f FakeOutPair) GetVal() string { return f.val }

func TestConfigValueForKey_FindsDifferentExistingKey(t *testing.T) {
	list := []editorconfig.OutPair{
		FakeOutPair{"alpha", "beta"},
		FakeOutPair{"gamma", "delta"},
	}
	got1 := editorconfig.ConfigValueForKey(list, "alpha")
	if got1 != "beta" {
		t.Errorf("Expected 'beta', got '%s'", got1)
	}
	got2 := editorconfig.ConfigValueForKey(list, "gamma")
	if got2 != "delta" {
		t.Errorf("Expected 'delta', got '%s'", got2)
	}
}

func TestConfigValueForKey_ReturnsEmptyForAnotherMissingKey(t *testing.T) {
	list := []editorconfig.OutPair{
		FakeOutPair{"one", "two"},
	}
	got := editorconfig.ConfigValueForKey(list, "absent")
	if got != "" {
		t.Errorf("Expected '', got '%s'", got)
	}
}

func TestConfigValueForKey_EmptyList_StillReturnsEmpty(t *testing.T) {
	list := []editorconfig.OutPair{}
	got := editorconfig.ConfigValueForKey(list, "doesnotexist")
	if got != "" {
		t.Errorf("Expected '', got '%s'", got)
	}
}

func TestConfigValueForKey_MultipleSameKeys_ReturnsFirstPublic(t *testing.T) {
	list := []editorconfig.OutPair{
		FakeOutPair{"dup", "uno"},
		FakeOutPair{"dup", "dos"},
		FakeOutPair{"other", "tres"},
	}
	got := editorconfig.ConfigValueForKey(list, "dup")
	if got != "uno" {
		t.Errorf("Expected 'uno', got '%s'", got)
	}
}

func TestInvalidConfigMessage_MakesCorrectStringPublic(t *testing.T) {
	msg := editorconfig.InvalidConfigMessage("42", "answer", "deepfile")
	expected := `"42" is not a valid value for key for file deepfile`
	if msg != expected {
		t.Errorf("Expected '%s', got '%s'", expected, msg)
	}
}

func TestAppliedConfigMessage_MakesCorrectStringPublic(t *testing.T) {
	msg := editorconfig.AppliedConfigMessage("enabled", "feature", "file.txt")
	expected := `Applied "enabled" as key for file file.txt`
	if msg != expected {
		t.Errorf("Expected '%s', got '%s'", expected, msg)
	}
}