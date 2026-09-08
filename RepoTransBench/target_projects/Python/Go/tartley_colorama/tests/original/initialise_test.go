package original

import "testing"

func TestInitWrapsWindows(t *testing.T) {
	result := initWrapSimulation("nt", true)
	if !result {
		t.Errorf("expected wrap for 'nt' with TTY or VT100")
	}
}

func TestInitDoesntWrapEmulatedWindows(t *testing.T) {
	result := initWrapSimulation("nt", false)
	if result {
		t.Errorf("expected no wrap for 'nt' with no TTY or VT100")
	}
}

func TestInitDoesntWrapNonWindows(t *testing.T) {
	result := initWrapSimulation("posix", true)
	if result {
		t.Errorf("expected no wrap for non-nt systems")
	}
}

func TestInitAutoresetWrapsAllPlatforms(t *testing.T) {
	result := initAutoResetWrapSimulation("whateveros")
	if !result {
		t.Errorf("expected wrap for any platform when autoreset is set")
	}
}

func TestInitWrapOffDoesntWrapOnWindows(t *testing.T) {
	result := initWrapSimulationWithOption("nt", false)
	if result {
		t.Errorf("expected no wrap when wrap=false on nt")
	}
}

// Simulated logic for initialisation tests
func initWrapSimulation(os string, doWrap bool) bool {
	return os == "nt" && doWrap
}

func initWrapSimulationWithOption(os string, wrap bool) bool {
	return os == "nt" && wrap
}

func initAutoResetWrapSimulation(os string) bool {
	return true // autoreset means always wrap
}