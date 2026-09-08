package public_tests

import (
	"strings"
	"testing"
)

func parseVersion(vstr string) (int, int, int) {
	// Parse "Coq 8.15.0 (Feb 2022)" style
	vstr = strings.TrimPrefix(vstr, "Coq ")
	vstr = strings.Fields(vstr)[0]
	parts := strings.SplitN(vstr, ".", 3)
	major, minor, patch := 0, 0, 0
	if len(parts) > 0 {
		fmtSscanf(parts[0], "%d", &major)
	}
	if len(parts) > 1 {
		minorStr := parts[1]
		for j := 0; j < len(minorStr) && '0' <= minorStr[j] && minorStr[j] <= '9'; j++ {
			minor = minor*10 + int(minorStr[j]-'0')
		}
	}
	if len(parts) > 2 {
		patchStr := parts[2]
		for j := 0; j < len(patchStr) && '0' <= patchStr[j] && patchStr[j] <= '9'; j++ {
			patch = patch*10 + int(patchStr[j]-'0')
		}
	}
	return major, minor, patch
}

func compareVersion(a, b [3]int) int {
	for i := 0; i < 3; i++ {
		if a[i] < b[i] {
			return -1
		}
		if a[i] > b[i] {
			return 1
		}
	}
	return 0
}

func TestPublicParseVersionMinor(t *testing.T) {
	vstr := "Coq 8.15.0 (Feb 2022)"
	major, minor, _ := parseVersion(vstr)
	if major != 8 || minor != 15 {
		t.Errorf("Expected (8,15,?), got (%v,%v)", major, minor)
	}
}

func TestPublicVersionCompareGreaterMajor(t *testing.T) {
	a := [3]int{8, 17, 0}
	b := [3]int{8, 16, 5}
	if compareVersion(a, b) <= 0 {
		t.Errorf("Expected %v > %v", a, b)
	}
}

func TestPublicVersionCompareSmallerMinor(t *testing.T) {
	a := [3]int{8, 7, 1}
	b := [3]int{8, 8, 0}
	if compareVersion(a, b) >= 0 {
		t.Errorf("Expected %v < %v", a, b)
	}
}