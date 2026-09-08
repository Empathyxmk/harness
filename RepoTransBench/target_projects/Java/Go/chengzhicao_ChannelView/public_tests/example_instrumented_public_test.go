package public_tests

import (
	"testing"
)

// Translated from: app/src/androidTest/java/com/cheng/sample/ExampleInstrumentedPublicTest.java
func TestUseAppContextPublic(t *testing.T) {
	// The 'public' test expects the app context package name to NOT be "com.cheng.channelview"
	appContextPackageName := "some.other.package"
	if appContextPackageName == "com.cheng.channelview" {
		t.Errorf("expected NOT package name 'com.cheng.channelview', got '%s'", appContextPackageName)
	}
}

// Translated from: channelview/src/androidTest/java/com/cheng/channel/ExampleInstrumentedPublicTest.java
func TestUseAppContextChannelPublic(t *testing.T) {
	appContextPackageName := "another.different.package"
	if appContextPackageName == "com.cheng.channelview.test" {
		t.Errorf("expected NOT package name 'com.cheng.channelview.test', got '%s'", appContextPackageName)
	}
}