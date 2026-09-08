package public_tests

import (
	"fmt"
	"testing"
)

func wizMdnsName(mac string) string {
	return fmt.Sprintf("WIZ_%s._wiz._udp.local.", mac)
}
func defaultMac(ip string, port int) string {
	octets := netParseIP(ip)
	return fmt.Sprintf("%02X%02X%02X%02X%04X", octets[0], octets[1], octets[2], octets[3], port)
}

func netParseIP(ip string) []byte {
	var o [4]byte
	fmt.Sscanf(ip, "%d.%d.%d.%d", &o[0], &o[1], &o[2], &o[3])
	return o[:]
}

func TestWizMdnsNamePublic(t *testing.T) {
	mac := "112233445566"
	got := wizMdnsName(mac)
	want := "WIZ_112233445566._wiz._udp.local."
	if got != want {
		t.Errorf("wizMdnsName returned %s, want %s", got, want)
	}
}

func TestDefaultMacPublic(t *testing.T) {
	ip := "192.168.2.22"
	port := 9020
	mac := defaultMac(ip, port)
	want := "C0A80216232C"
	if mac != want {
		t.Errorf("defaultMac(%s, %d) = %s, want %s", ip, port, mac, want)
	}
}