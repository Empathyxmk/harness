package public_tests

import (
	"testing"
	"mattupstate_overholt/overholt/settings"
)

func TestSettingsPublicValues(t *testing.T) {
	if len(settings.SECRET_KEY) < 8 {
		t.Errorf("SECRET_KEY length should be >= 8, got %d", len(settings.SECRET_KEY))
	}
	if settings.DEBUG != true && settings.DEBUG != false {
		t.Errorf("DEBUG should be a boolean value")
	}
	if settings.SECURITY_SEND_REGISTER_EMAIL != true && settings.SECURITY_SEND_REGISTER_EMAIL != false {
		t.Errorf("SECURITY_SEND_REGISTER_EMAIL should be a boolean value")
	}
}