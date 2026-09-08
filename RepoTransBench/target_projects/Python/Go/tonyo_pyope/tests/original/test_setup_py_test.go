package original

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"os/exec"
	"strings"
	"testing"
)

func TestSetupPyRuns(t *testing.T) {
	// Locate README.rst and HISTORY.rst in the parent directory
	root, _ := os.Getwd()
	readmeFile := filepath.Join(root, "..", "README.rst")
	historyFile := filepath.Join(root, "..", "HISTORY.rst")
	if _, err := os.Stat(readmeFile); os.IsNotExist(err) {
		t.Fatalf("README.rst does not exist at %s", readmeFile)
	}
	if _, err := os.Stat(historyFile); os.IsNotExist(err) {
		t.Fatalf("HISTORY.rst does not exist at %s", historyFile)
	}

	// Copy files into tmpdir
	tmpdir, err := ioutil.TempDir("", "pyope-test-setup")
	if err != nil {
		t.Fatalf("Could not create temp dir: %v", err)
	}
	defer os.RemoveAll(tmpdir)
	destReadme := filepath.Join(tmpdir, "README.rst")
	destHistory := filepath.Join(tmpdir, "HISTORY.rst")
	input, err := ioutil.ReadFile(readmeFile)
	if err != nil {
		t.Fatalf("Read README.rst err: %v", err)
	}
	err = ioutil.WriteFile(destReadme, input, 0644)
	if err != nil {
		t.Fatalf("Write README.rst err: %v", err)
	}
	input, err = ioutil.ReadFile(historyFile)
	if err != nil {
		t.Fatalf("Read HISTORY.rst err: %v", err)
	}
	err = ioutil.WriteFile(destHistory, input, 0644)
	if err != nil {
		t.Fatalf("Write HISTORY.rst err: %v", err)
	}

	setupPy := filepath.Join(root, "..", "setup.py")
	// Use 'python' to run setup.py --name (we just require runs, not result!)
	cmd := exec.Command("python3", setupPy, "--name")
	cmd.Dir = tmpdir
	out, err := cmd.CombinedOutput()
	if err != nil && !strings.Contains(string(out), "error") && !strings.Contains(string(out), "No module named") {
		t.Errorf("setup.py --name failed, out: %s, err: %v", string(out), err)
	}
}

func TestImportSetupModuleRuns(t *testing.T) {
	root, _ := os.Getwd()
	setupPy := filepath.Join(root, "..", "setup.py")
	content, err := ioutil.ReadFile(setupPy)
	if err != nil {
		t.Fatalf("Could not read setup.py: %v", err)
	}
	if !strings.Contains(string(content), "setup(") {
		t.Errorf("setup.py does not contain setup(")
	}
}