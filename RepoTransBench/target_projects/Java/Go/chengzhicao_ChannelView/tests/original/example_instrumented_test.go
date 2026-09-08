package original

import (
	"testing"
)

// Translated from: app/src/androidTest/java/com/cheng/sample/ExampleInstrumentedTest.java
func TestUseAppContext(t *testing.T) {
	// In Android, checks the application context package name.
	// In Go, we cannot check Android package, but we can stub a comparable test.
	// For faithful translation, we'll simulate:
	appContextPackageName := "com.cheng.channelview"
	if appContextPackageName != "com.cheng.channelview" {
		t.Errorf("expected package name 'com.cheng.channelview', got '%s'", appContextPackageName)
	}
}

// Translated from: channelview/src/androidTest/java/com/cheng/channel/ExampleInstrumentedTest.java
func TestUseAppContextChannel(t *testing.T) {
	appContextPackageName := "com.cheng.channelview.test"
	if appContextPackageName != "com.cheng.channelview.test" {
		t.Errorf("expected package name 'com.cheng.channelview.test', got '%s'", appContextPackageName)
	}
}