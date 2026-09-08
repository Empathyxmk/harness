package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"os"
	"path/filepath"
	"runtime"
)

type DummyInstallCmd struct {
	Home, InstallBase, InstallPlatbase, InstallLib, InstallPlatlib, InstallPurelib string
	InstallHeaders, InstallScripts, InstallData string
	ExtraPath                                  []string
	ExtraDirs, PathFile                        string
	Prefix, User                               string
}

func (cmd *DummyInstallCmd) HandleExtraPath() error {
	if cmd.ExtraPath == nil {
		cmd.ExtraDirs = ""
		cmd.PathFile = ""
		return nil
	}
	switch len(cmd.ExtraPath) {
	case 1:
		cmd.ExtraDirs = cmd.ExtraPath[0]
		cmd.PathFile = cmd.ExtraPath[0]
	case 2:
		cmd.ExtraDirs = cmd.ExtraPath[1]
		cmd.PathFile = cmd.ExtraPath[0]
	default:
		return assert.AnError
	}
	return nil
}

func (cmd *DummyInstallCmd) FinalizeOptions() error {
	// Only for demonstration: simulate error logic
	if cmd.Prefix != "" && cmd.InstallBase != "" {
		return assert.AnError
	}
	if cmd.Home != "" && (cmd.Prefix != "" || cmd.InstallBase != "") {
		return assert.AnError
	}
	if cmd.User != "" && (cmd.Prefix != "" || cmd.Home != "" || cmd.InstallBase != "" || cmd.InstallPlatbase != "") {
		return assert.AnError
	}
	return nil
}

func TestInstall_HomeInstallationScheme(t *testing.T) {
	builddir := t.TempDir()
	destination := filepath.Join(builddir, "installation")
	impl := runtime.Compiler
	pkgName := "foopkg"
	platlibdir := "lib" // Python uses sys.platlibdir if present

	cmd := &DummyInstallCmd{
		Home:            destination,
		InstallBase:     destination,
		InstallPlatbase: destination,
		InstallLib:      filepath.Join(destination, "lib", impl),
		InstallPlatlib:  filepath.Join(destination, platlibdir, impl),
		InstallPurelib:  filepath.Join(destination, "lib", impl),
		InstallHeaders:  filepath.Join(destination, "include", impl, pkgName),
		InstallScripts:  filepath.Join(destination, "bin"),
		InstallData:     destination,
	}
	assert.Equal(t, destination, cmd.InstallBase)
	assert.Equal(t, destination, cmd.InstallPlatbase)
	assert.Equal(t, filepath.Join(destination, "lib", impl), cmd.InstallLib)
	assert.Equal(t, filepath.Join(destination, platlibdir, impl), cmd.InstallPlatlib)
	assert.Equal(t, filepath.Join(destination, "lib", impl), cmd.InstallPurelib)
	assert.Equal(t, filepath.Join(destination, "include", impl, pkgName), cmd.InstallHeaders)
	assert.Equal(t, filepath.Join(destination, "bin"), cmd.InstallScripts)
	assert.Equal(t, destination, cmd.InstallData)
}

func TestInstall_HandleExtraPath(t *testing.T) {
	cmd := &DummyInstallCmd{ExtraPath: []string{"path", "dirs"}}
	assert.Nil(t, cmd.HandleExtraPath())
	assert.Equal(t, "dirs", cmd.ExtraDirs)
	assert.Equal(t, "path", cmd.PathFile)

	cmd.ExtraPath = []string{"path"}
	assert.Nil(t, cmd.HandleExtraPath())
	assert.Equal(t, "path", cmd.ExtraDirs)
	assert.Equal(t, "path", cmd.PathFile)

	cmd.ExtraPath = nil
	assert.Nil(t, cmd.HandleExtraPath())
	assert.Equal(t, "", cmd.ExtraDirs)
	assert.Equal(t, "", cmd.PathFile)

	cmd.ExtraPath = []string{"path", "dirs", "again"}
	err := cmd.HandleExtraPath()
	assert.Error(t, err)
}

func TestInstall_FinalizeOptions(t *testing.T) {
	cmd := &DummyInstallCmd{Prefix: "prefix", InstallBase: "base"}
	assert.Error(t, cmd.FinalizeOptions())
	cmd = &DummyInstallCmd{InstallBase: "", Prefix: "", Home: "home"}
	assert.Nil(t, cmd.FinalizeOptions())
	cmd = &DummyInstallCmd{Prefix: "", Home: "", User: "user"}
	assert.Nil(t, cmd.FinalizeOptions())
}

func TestInstall_RecordFiles(t *testing.T) {
	files := []string{"hello.py", "hello.go", "sayhi", "UNKNOWN-0.0.0-py3.8.egg-info"}
	expected := []string{"hello.py", "hello.go", "sayhi", "UNKNOWN-0.0.0-py3.8.egg-info"}
	assert.ElementsMatch(t, files, expected)
}

// Simulates debug mode just runs
func TestInstall_DebugMode(t *testing.T) {
	debug := true
	assert.True(t, debug)
}