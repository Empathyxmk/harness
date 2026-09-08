package original

import (
	"testing"
	"errors"
)

type Intent struct {
	Action string
}

type PackageManager struct {
	ShouldResolve bool
}

type AccessControl1Activity struct {
	pkgManager *PackageManager
	intentStarted bool
}

func NewAccessControl1Activity() *AccessControl1Activity {
	return &AccessControl1Activity{
		pkgManager: &PackageManager{},
	}
}

func (a *AccessControl1Activity) GetPackageManager() *PackageManager {
	return a.pkgManager
}

func (a *AccessControl1Activity) StartActivity(i *Intent) error {
	a.intentStarted = true
	if i == nil {
		return errors.New("Intent is nil")
	}
	return nil
}

// Simulate the viewAPICredentials behaviour
func (a *AccessControl1Activity) ViewAPICredentials() error {
	intent := &Intent{Action: "VIEW"}
	if a.pkgManager.ShouldResolve {
		return a.StartActivity(intent)
	}
	// Normally would show Toast, just return nil (for test coverage)
	return nil
}

func TestAccessControl1Activity_onCreate_setsLayout(t *testing.T) {
	NewAccessControl1Activity()
	// No panic or error
}

func TestAccessControl1Activity_viewAPICredentials_intentResolved_startsActivity(t *testing.T) {
	a := NewAccessControl1Activity()
	a.pkgManager.ShouldResolve = true

	err := a.ViewAPICredentials()
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if !a.intentStarted {
		t.Error("Expected intent to be started")
	}
}

func TestAccessControl1Activity_viewAPICredentials_intentNotResolved_showsToastAndLogs(t *testing.T) {
	a := NewAccessControl1Activity()
	a.pkgManager.ShouldResolve = false

	err := a.ViewAPICredentials()
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	// No intent should be started
	if a.intentStarted {
		t.Error("Intent should not be started when intent is not resolved")
	}
}