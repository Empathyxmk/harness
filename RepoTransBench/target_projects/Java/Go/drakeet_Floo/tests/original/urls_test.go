package original

import "testing"

func IsRemoteUrl(s string) bool {
	return len(s) > 7 && (s[:7] == "http://" || s[:8] == "https://")
}
func IsLocalUrl(s string) bool {
	return len(s) > 7 && (s[:7] == "file://" || s[:10] == "content://")
}

func TestIsRemoteUrl(t *testing.T) {
	cases := []struct {
		Input    string
		Expected bool
	}{
		{"http://example.com", true},
		{"https://secure.com", true},
		{"file://local.txt", false},
		{"content://file", false},
		{"", false},
		{ // null (not possible, but let's handle zero value)
			"", false,
		},
	}
	for _, c := range cases {
		got := IsRemoteUrl(c.Input)
		if got != c.Expected {
			t.Errorf("IsRemoteUrl(%v) = %v; want %v", c.Input, got, c.Expected)
		}
	}
}

func TestIsLocalUrl(t *testing.T) {
	cases := []struct {
		Input    string
		Expected bool
	}{
		{"file://localfile.txt", true},
		{"content://local", true},
		{"http://remote.net", false},
		{"https://secure.com", false},
		{"", false},
	}
	for _, c := range cases {
		got := IsLocalUrl(c.Input)
		if got != c.Expected {
			t.Errorf("IsLocalUrl(%v) = %v; want %v", c.Input, got, c.Expected)
		}
	}
}