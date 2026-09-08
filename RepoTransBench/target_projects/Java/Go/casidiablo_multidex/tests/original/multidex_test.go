package original

import (
	"testing"
)

func isVMMultidexCapable(vmVersion string) bool {
	// Ported logic from Java: null, empty, or <2.1 (major,minor) returns false.
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

func TestVersionCheck(t *testing.T) {
	type testpair struct{ vm string; want bool }
	cases := []testpair{
		{vm: "", want: false},
		{vm: "-1.32.54", want: false},
		{vm: "1.32.54", want: false},
		{vm: "1.32", want: false},
		{vm: "2.0", want: false},
		{vm: "2.000.1254", want: false},
		{vm: "2.1.1254", want: true},
		{vm: "2.1", want: true},
		{vm: "2.2", want: true},
		{vm: "2.1.0000", want: true},
		{vm: "2.2.0000", want: true},
		{vm: "002.0001.0010", want: true}, // allow leading zeros
		{vm: "3.0", want: true},
		{vm: "3.0.0", want: true},
		{vm: "3.0.1", want: true},
		{vm: "3.1.0", want: true},
		{vm: "03.1.132645", want: true},
		{vm: "03.2", want: true},
	}
	for _, c := range cases {
		got := isVMMultidexCapable(c.vm)
		if got != c.want {
			t.Errorf("isVMMultidexCapable(%q) = %v, want %v", c.vm, got, c.want)
		}
	}
}