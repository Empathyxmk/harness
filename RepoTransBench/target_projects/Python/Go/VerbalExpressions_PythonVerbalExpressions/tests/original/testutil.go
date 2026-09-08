package original

import "regexp"

// stringContains reports whether substr is within s.
func stringContains(s, substr string) bool {
	return regexp.MustCompile(regexp.QuoteMeta(substr)).FindStringIndex(s) != nil
}