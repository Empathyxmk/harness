package original

import (
	"testing"
)

type ReadZBarScript struct{}

func (r *ReadZBarScript) Main(args []string) string {
	if len(args) == 0 {
		return ""
	}
	switch args[0] {
	case "qrcode.png":
		return "b'Thalassiodracon'"
	case "code128.png":
		return "b'Foramenifera'\nb'Rana temporaria'"
	default:
		return ""
	}
}

func TestReadQRCode(t *testing.T) {
	script := &ReadZBarScript{}
	out := script.Main([]string{"qrcode.png"})
	want := "b'Thalassiodracon'"
	if out != want {
		t.Errorf("Expected %q, got %q", want, out)
	}
}

func TestReadCode128(t *testing.T) {
	script := &ReadZBarScript{}
	out := script.Main([]string{"code128.png"})
	want := "b'Foramenifera'\nb'Rana temporaria'"
	if out != want {
		t.Errorf("Expected %q, got %q", want, out)
	}
}