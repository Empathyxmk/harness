package original

import (
	"testing"

	"editorconfig"
)

// FakeOutPair implements editorconfig.OutPair for tests
type FakeOutPair struct {
	key string
	val string
}

func (f FakeOutPair) GetKey() string { return f.key }
func (f FakeOutPair) GetVal() string { return f.val }

func TestConfigValueForKey_FindsExistingKey(t *testing.T) {
	list := []editorconfig.OutPair{
		FakeOutPair{"foo", "bar"},
		FakeOutPair{"baz", "qux"},
	}
	got1 := editorconfig.ConfigValueForKey(list, "foo")
	if got1 != "bar" {
		t.Errorf("Expected 'bar', got '%s'", got1)
	}
	got2 := editorconfig.ConfigValueForKey(list, "baz")
	if got2 != "qux" {
		t.Errorf("Expected 'qux', got '%s'", got2)
	}
}

func TestConfigValueForKey_ReturnsEmptyForMissingKey(t *testing.T) {
	list := []editorconfig.OutPair{
		FakeOutPair{"foo", "bar"},
	}
	got := editorconfig.ConfigValueForKey(list, "notfound")
	if got != "" {
		t.Errorf("Expected '', got '%s'", got)
	}
}

func TestConfigValueForKey_EmptyList(t *testing.T) {
	list := []editorconfig.OutPair{}
	got := editorconfig.ConfigValueForKey(list, "foo")
	if got != "" {
		t.Errorf("Expected '', got '%s'", got)
	}
}

func TestConfigValueForKey_MultipleSameKeys_ReturnsFirst(t *testing.T) {
	list := []editorconfig.OutPair{
		FakeOutPair{"foo", "first"},
		FakeOutPair{"foo", "second"},
		FakeOutPair{"bar", "other"},
	}
	got := editorconfig.ConfigValueForKey(list, "foo")
	if got != "first" {
		t.Errorf("Expected 'first', got '%s'", got)
	}
}

func TestInvalidConfigMessage_MakesCorrectString(t *testing.T) {
	msg := editorconfig.InvalidConfigMessage("value", "key", "file")
	expected := `"value" is not a valid value for key for file file`
	if msg != expected {
		t.Errorf("Expected '%s', got '%s'", expected, msg)
	}
}

func TestAppliedConfigMessage_MakesCorrectString(t *testing.T) {
	msg := editorconfig.AppliedConfigMessage("value", "key", "file")
	expected := `Applied "value" as key for file file`
	if msg != expected {
		t.Errorf("Expected '%s', got '%s'", expected, msg)
	}
}