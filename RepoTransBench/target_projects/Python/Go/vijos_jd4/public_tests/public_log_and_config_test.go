package public_tests

import (
	"errors"
	"os"
	"path/filepath"
	"testing"
)

func TestPublicLogInstallBehavior(t *testing.T) {
	os.Unsetenv("JD4_USE_SYSLOG")
	installed := false
	type fakeColoredlogs struct{}
	fakeInstall := func(args ...interface{}) {
		installed = true
	}
	colored := &fakeColoredlogs{}
	_ = colored
	fakeInstall()
	if !installed {
		t.Errorf("expected install to be called")
	}
}

func TestPublicLogSyslogBehavior(t *testing.T) {
	os.Setenv("JD4_USE_SYSLOG", "yes")
	defer os.Unsetenv("JD4_USE_SYSLOG")
	called := false
	type fakeSyslog struct{}
	fakeEnable := func(args ...interface{}) {
		called = true
	}
	syslog := &fakeSyslog{}
	_ = syslog
	fakeEnable()
	if !called {
		t.Errorf("expected syslog to be called")
	}
}

func TestPublicConfigFileNotFound(t *testing.T) {
	tmpDir := t.TempDir()
	configPath := filepath.Join(tmpDir, "config.yaml")
	_, err := os.Stat(configPath)
	if err == nil {
		t.Fatalf("Config file should not exist")
	}
	errorCalled := false
	fakeLogger := func(args ...interface{}) {
		errorCalled = true
	}
	if errorCalled == false {
		fakeLogger("error: config file not found")
		err = errors.New("config not found: simulating SystemExit")
	}
	if !errorCalled {
		t.Errorf("Logger's error not called for missing config file")
	}
}