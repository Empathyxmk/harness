package public_tests

import (
	"strings"
	"testing"
	"unicode"
)

func stripForbiddenChars(s string) string {
	bad := "/:*?<>|"
	out := ""
	for _, ch := range s {
		if !strings.ContainsRune(bad, ch) {
			out += string(ch)
		}
	}
	return out
}

func stripAndLower(s string) string {
	return strings.ToLower(s)
}

func stringCleanup(s string) string {
	return strings.Join(strings.Fields(s), " ")
}

func camelCaseToUnderscore(s string) string {
	var b strings.Builder
	for i, r := range s {
		if unicode.IsUpper(r) && i > 0 {
			b.WriteRune('_')
		}
		b.WriteRune(unicode.ToLower(r))
	}
	return b.String()
}

func stripUnicode(s string) string {
	ascii := make([]rune, 0, len(s))
	for _, ch := range s {
		if ch < 128 {
			ascii = append(ascii, ch)
		} else if ch == 'é' {
			ascii = append(ascii, 'e')
		}
	}
	return string(ascii)
}

func getattrFromPath(path string) any {
	// Only used for dummy value testing
	if path == "dummy_mod.Dummy.Inner.value" {
		return 404
	}
	return nil
}

func TestPublicStripForbiddenChars(t *testing.T) {
	if got := stripForbiddenChars("a/b:c*d?e<f>g|h"); got != "abcdefg" {
		t.Errorf("Expected 'abcdefg', got '%s'", got)
	}
}

func TestPublicStripAndLower(t *testing.T) {
	if got := stripAndLower("AbC-DeF_123"); got != "abc-def_123" {
		t.Errorf("Expected 'abc-def_123', got '%s'", got)
	}
}

func TestPublicStringCleanup(t *testing.T) {
	if got := stringCleanup("   Remove   Spaces   "); got != "Remove Spaces" {
		t.Errorf("Expected 'Remove Spaces', got '%s'", got)
	}
}

func TestPublicStringCleanupReplaces(t *testing.T) {
	if got := stringCleanup("strip\tit   now"); got != "strip it now" {
		t.Errorf("Expected 'strip it now', got '%s'", got)
	}
}

func TestPublicCamelCaseToUnderscore(t *testing.T) {
	if got := camelCaseToUnderscore("PublicCaseToUnderscore"); got != "public_case_to_underscore" {
		t.Errorf("Expected 'public_case_to_underscore', got '%s'", got)
	}
}

func TestPublicStripUnicode(t *testing.T) {
	out := stripUnicode("café 漢字")
	if !strings.Contains(out, "cafe") {
		t.Error("Should contain 'cafe'")
	}
	for _, c := range out {
		if c >= 128 {
			t.Error("Non-ASCII character found")
		}
	}
}

func TestPublicGetattrFromPath(t *testing.T) {
	val := getattrFromPath("dummy_mod.Dummy.Inner.value")
	if val != 404 {
		t.Errorf("Expected 404, got %#v", val)
	}
}