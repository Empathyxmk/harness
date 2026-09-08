package original

import (
	"testing"
	"mattupstate_overholt/overholt/settings"
)

func TestSettingsValues(t *testing.T) {
	if settings.DEBUG != true {
		t.Errorf("Expected settings.DEBUG=true, got %v", settings.DEBUG)
	}
	if settings.SECRET_KEY != "super-secret-key" {
		t.Errorf("Expected settings.SECRET_KEY = 'super-secret-key', got '%s'", settings.SECRET_KEY)
	}
	if settings.SECURITY_SEND_REGISTER_EMAIL != false {
		t.Errorf("Expected settings.SECURITY_SEND_REGISTER_EMAIL = false, got %v", settings.SECURITY_SEND_REGISTER_EMAIL)
	}
}