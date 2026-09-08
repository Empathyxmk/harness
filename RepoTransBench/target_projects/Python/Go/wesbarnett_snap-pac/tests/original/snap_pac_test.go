package original

import (
	"os"
	"path/filepath"
	"testing"
	"io/ioutil"

	"wesbarnett_snap_pac/scripts"
)

type dummyPopenResult struct {
	retstr string
}

func (d dummyPopenResult) Read() string {
	return d.retstr
}

func fakePopenFactory(retval string) func(string) dummyPopenResult {
	return func(cmd string) dummyPopenResult {
		return dummyPopenResult{retval}
	}
}

func TestSnapperCmdStrAndCall(t *testing.T) {
	cmd := scripts.NewSnapperCmd("root", "pre", "number", "desc", true, intPtr(123), "ud")
	s := cmd.String()
	if !strings.Contains(s, "--no-dbus") ||
		!strings.Contains(s, "--config root create") ||
		!strings.Contains(s, "--description \"desc\"") ||
		!strings.Contains(s, "--userdata \"ud\"") ||
		!strings.Contains(s, "--type pre") {
		t.Errorf("SnapperCmd string missing expected components: %s", s)
	}
	// Simulated call using dummy popen
	res := fakePopenFactory("42\n")(cmd.String())
	if res.Read() != "42\n" {
		t.Errorf("SnapperCmd simulated call output: got %q want %q", res.Read(), "42\n")
	}
}

func TestSnapperCmdPostNoPrenumber(t *testing.T) {
	cmd := scripts.NewSnapperCmd("root", "post", "number", "", false, nil, "")
	typStr := cmd.String()
	if !strings.Contains(typStr, "--type single") && !strings.Contains(typStr, "--type post") {
		t.Errorf("SnapperCmd type string missing '--type single' or '--type post': %s", typStr)
	}
	fakePopenFactory("test")(cmd.String())
}

func TestConfigProcessorDefaultSettings(t *testing.T) {
	tmpdir, err := ioutil.TempDir("", "snapper-defaults")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tmpdir)
	inifile := filepath.Join(tmpdir, "config.ini")
	ioutil.WriteFile(inifile, []byte(""), 0644)
	cp, err := scripts.NewConfigProcessor(inifile, "pre", "parent", []string{"pkg1", "pkg2"})
	if err != nil {
		t.Fatal(err)
	}
	result := cp.Process("root")
	desc, ok := result["description"].(string)
	if !ok || !strings.HasPrefix(desc, "parent") {
		t.Errorf("default config processor output: %v", desc)
	}
	ca, ok := result["cleanup_algorithm"].(string)
	if !ok || ca != "number" {
		t.Errorf("cleanup_algorithm got '%s', want 'number'", ca)
	}
}

func TestConfigProcessorIniOptions(t *testing.T) {
	tmpdir, err := ioutil.TempDir("", "snapper-iniopt")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tmpdir)
	inifile := filepath.Join(tmpdir, "ext.ini")
	configTxt := `
[DEFAULT]
snapshot = false
cleanup_algorithm = timeline
pre_description = mycmd
post_description = install packages
desc_limit = 5
important_packages = ["imp"]
important_commands = ["imp_cmd"]
userdata = ["mytag"]
[root]
snapshot = true
`
	ioutil.WriteFile(inifile, []byte(configTxt), 0644)
	cp, err := scripts.NewConfigProcessor(inifile, "pre", "imp_cmd", []string{"imp", "unimp"})
	if err != nil {
		t.Fatal(err)
	}
	if ca := cp.GetCleanupAlgorithm("root"); ca != "timeline" {
		t.Errorf("expected cleanup_algorithm 'timeline', got '%s'", ca)
	}
	if desc := cp.GetDescription("root"); desc != "mycmd" {
		t.Errorf("desc_limit trimming error: got '%s'", desc)
	}
	if !cp.CheckImportantCommands("root") {
		t.Errorf("important command detection failed")
	}
	if !cp.CheckImportantPackages("root") {
		t.Errorf("important package detection failed")
	}
	ud := cp.GetUserdata("root")
	if !strings.Contains(ud, "important=yes") || !strings.Contains(ud, "mytag") {
		t.Errorf("userdata tag missing: got '%s'", ud)
	}
	out := cp.Process("root")
	if _, ok := out["description"]; !ok {
		t.Error("output missing 'description'")
	}
	if _, ok := out["userdata"]; !ok {
		t.Error("output missing 'userdata'")
	}
}

func TestConfigProcessorNonexistentSection(t *testing.T) {
	tmpdir, err := ioutil.TempDir("", "snapper-nosec")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tmpdir)
	inifile := filepath.Join(tmpdir, "spawn.ini")
	ioutil.WriteFile(inifile, []byte(""), 0644)
	cp, err := scripts.NewConfigProcessor(inifile, "post", "irrelevant", []string{})
	if err != nil {
		t.Fatal(err)
	}
	rv := cp.Process("not_here")
	if _, ok := rv["snapshot"]; !ok {
		t.Error("config processor output missing snapshot field")
	}
}

func TestConfigProcessorCheckImportant(t *testing.T) {
	tmpdir, err := ioutil.TempDir("", "snapper-impcmd")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tmpdir)
	inifile := filepath.Join(tmpdir, "imp2.ini")
	content := `
[root]
snapshot = true
important_packages = ["pkgx"]
important_commands = ["cmdy"]
userdata = ["z"]
`
	ioutil.WriteFile(inifile, []byte(content), 0644)
	cp, err := scripts.NewConfigProcessor(inifile, "post", "cmdy", []string{"pkgx", "pkgother"})
	if err != nil {
		t.Fatal(err)
	}
	rv := cp.CheckImportant("root")
	if !rv {
		t.Errorf("important check should be true")
	}
}

func TestConfigProcessorNoImportant(t *testing.T) {
	tmpdir, err := ioutil.TempDir("", "snapper-noimp")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tmpdir)
	inifile := filepath.Join(tmpdir, "noimp.ini")
	content := `
[root]
snapshot = true
important_packages = []
important_commands = []
userdata = []
`
	ioutil.WriteFile(inifile, []byte(content), 0644)
	cp, err := scripts.NewConfigProcessor(inifile, "post", "foo", []string{"bar"})
	if err != nil {
		t.Fatal(err)
	}
	if cp.CheckImportant("root") {
		t.Errorf("important check should be false")
	}
	if strings.Contains(cp.GetUserdata("root"), "important=yes") {
		t.Errorf("unexpected important tag in userdata")
	}
}

func TestSnapperCmdTypes(t *testing.T) {
	cmd := scripts.NewSnapperCmd("abc", "post", "alg", "", false, nil, "")
	str := cmd.String()
	if !strings.Contains(str, "--type single") && !strings.Contains(str, "--type post") {
		t.Error("SnapperCmd type string missing '--type single' or '--type post'")
	}
}