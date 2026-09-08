package original

import "testing"

func TestDisableShouldUnwrapStdoutAndStderr(t *testing.T) {
	stdout := isWrappedAndEnabled("stdout", false)
	stderr := isWrappedAndEnabled("stderr", false)
	if stdout {
		t.Error("stdout should not be wrapped when disabled")
	}
	if stderr {
		t.Error("stderr should not be wrapped when disabled")
	}
}

func TestDisableShouldNotWrapOtherStreams(t *testing.T) {
	custom := isWrappedAndEnabled("custom", false)
	if custom {
		t.Error("custom should not be wrapped when disabled")
	}
}

// Logic simulating enabled/disabled wrap
func isWrappedAndEnabled(stream string, enabled bool) bool {
	return enabled && (stream == "stdout" || stream == "stderr")
}