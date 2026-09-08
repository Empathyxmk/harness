package original

import "testing"

func TestShouldWrapStdoutAndStderr(t *testing.T) {
	wrappedStdout := isWrapped("stdout")
	wrappedStderr := isWrapped("stderr")
	if !wrappedStdout {
		t.Error("expected stdout to be wrapped")
	}
	if !wrappedStderr {
		t.Error("expected stderr to be wrapped")
	}
}

func TestShouldNotWrapOtherStreams(t *testing.T) {
	fakeStream := isWrapped("notStd")
	if fakeStream {
		t.Error("expected non-std streams to not be wrapped")
	}
}

// Dummy functions mimicking wrapping logic
func isWrapped(stream string) bool {
	return stream == "stdout" || stream == "stderr"
}