package public_tests

import "testing"

func isVMMultidexCapable(vmVersion string) bool {
	// Re-implementing logic from original.
	if len(vmVersion) == 0 {
		return false
	}
	var major, minor int
	parts := []byte(vmVersion)
	n, m := 0, 0
	for i := 0; i < len(parts) && parts[i] >= '0' && parts[i] <= '9'; i++ {
		n = n*10 + int(parts[i]-'0')
	}
	i := 0
	for i = 0; i < len(parts) && ((parts[i] >= '0' && parts[i] <= '9') || parts[i] == '.'); i++ {
		if parts[i] == '.' {
			i++
			break
		}
	}
	for ; i < len(parts) && parts[i] >= '0' && parts[i] <= '9'; i++ {
		m = m*10 + int(parts[i]-'0')
	}
	major, minor = n, m
	if major > 2 || (major == 2 && minor >= 1) {
		return true
	}
	return false
}

func TestVersionCheckPublic(t *testing.T) {
	type testpair struct{ vm string; want bool }
	cases := []testpair{
		// Null and malformed
		{vm: "0.9", want: false},
		{vm: "1.999.9999", want: false},
		{vm: "2.0.0", want: false},
		{vm: "2.0.1", want: false},
		// True for >=2.1.x
		{vm: "2.10", want: true},
		{vm: "2.1.1", want: true},
		{vm: "4.0", want: true},
		{vm: "10.2", want: true},
		{vm: "2.1.1.5", want: true},
		{vm: "2.2.12345", want: true},
		{vm: "05.5.5", want: true},
		// Edge, padded zeros
		{vm: "002.001.0001", want: true},
		{vm: "2.0.9999", want: false},
		{vm: "2.0.0000", want: false},
		{vm: "3.0.42", want: true},
	}
	for _, c := range cases {
		got := isVMMultidexCapable(c.vm)
		if got != c.want {
			t.Errorf("isVMMultidexCapable(%q) = %v, want %v", c.vm, got, c.want)
		}
	}
}