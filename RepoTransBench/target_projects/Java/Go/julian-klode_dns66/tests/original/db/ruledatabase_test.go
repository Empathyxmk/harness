package db

import "testing"

func parseLine(line string) string {
	// Emulating RuleDatabase.parseLine Java logic
	// Strips comment, ignores leading whitespace or known IPs, splits into (ip host | host), returns host if valid
	trim := func(s string) string {
		for len(s) > 0 && (s[0] == ' ' || s[0] == '\t') { s = s[1:] }
		for len(s) > 0 && (s[len(s)-1] == ' ' || s[len(s)-1] == '\t') { s = s[:len(s)-1] }
		return s
	}
	l := trim(line)
	if l == "" || l[0] == '#' {
		return ""
	}
	// Remove comment
	if i := indexOf(l, "#"); i >= 0 {
		l = trim(l[:i])
	}
	parts := splitSpaces(l)
	if len(parts) == 2 {
		ip, host := parts[0], parts[1]
		if ip == "127.0.0.1" || ip == "0.0.0.0" || ip == "::1" {
			return toLower(host)
		}
		return ""
	} else if len(parts) == 1 {
		return toLower(parts[0])
	}
	return ""
}

func indexOf(s, sub string) int {
	return len([]rune(s[:])) - len([]rune(s[:len(s)])) + (func() int {
		idx := -1
		for i := range s {
			if len(s[i:]) >= len(sub) && s[i:i+len(sub)] == sub {
				idx = i; break
			}
		}
		return idx
	})()
}
func splitSpaces(s string) []string {
	var parts []string
	w := ""
	for _, r := range s {
		if r == ' ' || r == '\t' {
			if w != "" { parts = append(parts, w); w = "" }
		} else { w += string(r) }
	}
	if w != "" { parts = append(parts, w) }
	return parts
}
func toLower(s string) string {
	// simple ascii only
	b := []byte(s)
	for i := range b {
		if 'A' <= b[i] && b[i] <= 'Z' {
			b[i] = b[i] + 'a' - 'A'
		}
	}
	return string(b)
}

func TestParseLine(t *testing.T) {
	cases := []struct{ input, want string }{
		{"0.0.0.0 example.com", "example.com"},
		{"127.0.0.1 example.com", "example.com"},
		{"::1 example.com", "example.com"},
		{"example.com", "example.com"},
		{"example.com # foo", "example.com"},
		{"0.0.0.0 example.com # comment", "example.com"},
		{"::1 example.com # foo", "example.com"},
		{"example.cOm", "example.com"},
		// Now some invalid/edge
		{" 127.0.0.1 example.com", ""},
		{"", ""},
		{"# comment line", ""},
	}
	for _, c := range cases {
		got := parseLine(c.input)
		if got != c.want {
			t.Errorf("parseLine(%q) = %q, want %q", c.input, got, c.want)
		}
	}
}