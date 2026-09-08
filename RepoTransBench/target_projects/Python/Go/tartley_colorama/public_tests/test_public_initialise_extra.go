package public_tests

import "testing"

func TestInitReturnsWrappedOnAllPlatformsWhenAutoresetPublic(t *testing.T) {
	cases := []struct {
		os    string
		hasVT bool
		isTTY bool
	}{
		{"nt", true, true},
		{"java", true, true},
		{"linux", true, true},
		{"osx", false, false},
	}
	for _, c := range cases {
		env := NewFakeEnv(c.os, c.hasVT, c.isTTY)
		out, err := env.InitWithAutoreset(true)
		if err != nil {
			t.Errorf("unexpected error: %v", err)
		}
		if !out.Wrapped {
			t.Errorf("expected Wrapped=true for os=%s", c.os)
		}
	}
}