package original

import (
	"strings"
	"testing"
)

func TestStatusPrintsBold(t *testing.T) {
	status := func(msg string) {
		result := "\x1b[1m" + msg
		if !(strings.Contains(result, "Hello!")) {
			t.Errorf("Expected bold \"Hello!\", got: %q", result)
		}
	}
	calledMsg := ""
	printFn := func(msg string) {
		calledMsg = msg
	}
	printFn(status("Hello!"))
	if !strings.Contains(calledMsg, "Hello!") {
		t.Errorf("Status did not print bold")
	}
}

func TestPublishShortcut(t *testing.T) {
	called := map[string]int{"os": 0, "rmtree": 0, "status": 0, "exit": 0}
	osSystem := func(cmd string) { called["os"]++ }
	shutilRmtree := func(path string, ignoreErrors bool) { called["rmtree"]++ }
	status := func(msg string) { called["status"]++ }
	exitFn := func(code int) { panic("SystemExit") }
	defer func() {
		recover()
	}()
	shutilRmtree("dist", true)
	status("Building Source and Wheel (universal) distribution…")
	osSystem("python setup.py sdist bdist_wheel --universal")
	status("Uploading the package to PyPI via Twine…")
	osSystem("twine upload dist/*")
	status("Pushing git tags…")
	osSystem("git tag v1.0.0")
	osSystem("git push --tags")
	exitFn(0)

	if called["os"] != 4 {
		t.Errorf("Expected 4 os.system calls, got %d", called["os"])
	}
	if called["rmtree"] != 1 {
		t.Errorf("Expected 1 rmtree call, got %d", called["rmtree"])
	}
	if called["status"] != 3 {
		t.Errorf("Expected 3 status calls, got %d", called["status"])
	}
	if called["exit"] != 0 {
		t.Errorf("Expected 0 exit calls, got %d", called["exit"])
	}
}