package public_tests

import (
	"testing"

	"apereo-cas-attack/casattack"
)

func containsCasLowerOnly(s string) bool {
	return s != "" && len(s) >= 3 && stringHasCasLower(s)
}

func stringHasCasLower(s string) bool {
	return s != "" && (len(s) >= 3) && (func() bool {
		for i := 0; i <= len(s)-3; i++ {
			if s[i:i+3] == "cas" {
				return true
			}
		}
		return false
	})()
}

func TestContainsCasSubstring_Public(t *testing.T) {
	for _, str := range []string{"this has cas inside", "xcasY", "casual"} {
		if !containsCasLowerOnly(str) {
			t.Errorf("Expected containsCasLowerOnly(%q) to be true", str)
		}
	}
}

func TestDoesNotContainCasSubstring_Public(t *testing.T) {
	for _, str := range []string{"CASE", "archive", "security"} {
		if containsCasLowerOnly(str) {
			t.Errorf("Expected containsCasLowerOnly(%q) to be false", str)
		}
	}
}

func TestPerformAttack_CasPresent_Public(t *testing.T) {
	target := "attackcas2024"
	expected := "Simulating CAS attack on attackcas2024"
	got := casattack.PerformAttack(target)
	if got != expected {
		t.Errorf("PerformAttack(%q) = %q, want %q", target, got, expected)
	}
}

func TestPerformAttack_CasAbsent_Public(t *testing.T) {
	target := "adminpanel"
	expected := "Target is not a CAS server: adminpanel"
	got := casattack.PerformAttack(target)
	if got != expected {
		t.Errorf("PerformAttack(%q) = %q, want %q", target, got, expected)
	}
}

func TestPerformAttack_OnlyCasWord_Public(t *testing.T) {
	target := "CaS"
	expected := "Target is not a CAS server: CaS"
	got := casattack.PerformAttack(target)
	if got != expected {
		t.Errorf("PerformAttack(%q) = %q, want %q", target, got, expected)
	}
}

func TestPerformAttack_CasInMiddle_Public(t *testing.T) {
	target := "alphaCasOmega"
	expected := "Target is not a CAS server: alphaCasOmega"
	got := casattack.PerformAttack(target)
	if got != expected {
		t.Errorf("PerformAttack(%q) = %q, want %q", target, got, expected)
	}
}

func TestPerformAttack_StartsWithCas_Public(t *testing.T) {
	target := "casualty"
	expected := "Simulating CAS attack on casualty"
	got := casattack.PerformAttack(target)
	if got != expected {
		t.Errorf("PerformAttack(%q) = %q, want %q", target, got, expected)
	}
}

func TestPerformAttack_EndsWithCas_Public(t *testing.T) {
	target := "smartsystems.cas"
	expected := "Simulating CAS attack on smartsystems.cas"
	got := casattack.PerformAttack(target)
	if got != expected {
		t.Errorf("PerformAttack(%q) = %q, want %q", target, got, expected)
	}
}

func TestPerformAttack_CasLikeButNotCAS_Public(t *testing.T) {
	target := "CASE"
	expected := "Target is not a CAS server: CASE"
	got := casattack.PerformAttack(target)
	if got != expected {
		t.Errorf("PerformAttack(%q) = %q, want %q", target, got, expected)
	}
}

func TestPerformAttack_EmptyString_Public(t *testing.T) {
	target := ""
	expected := "Target is not a CAS server: "
	got := casattack.PerformAttack(target)
	if got != expected {
		t.Errorf("PerformAttack(%q) = %q, want %q", target, got, expected)
	}
}