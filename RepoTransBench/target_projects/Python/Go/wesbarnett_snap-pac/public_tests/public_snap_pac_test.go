package public_tests

import (
	"os"
	"path/filepath"
	"strings"
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

func TestPublicSnapperCmdStrAndCall(t *testing.T) {
	cmd := scripts.NewSnapperCmd("data", "pre", "timeline", "my-desc", true, intPtr(789), "user_data")
	s := cmd.String()
	if !strings.Contains(s, "--no-dbus") ||
		!strings.Contains(s, "--config data create") ||
		!strings.Contains(s, "--description \"my-desc\"") ||
		!strings.Contains(s, "--userdata \"user_data\"") ||
		!strings.Contains(s, "--type pre") {
		t.Errorf("SnapperCmd string missing expected components: %s", s)
	}
	// Simulated call using dummy popen
	res := fakePopenFactory("314\n")(cmd.String())
	if res.Read() != "314\n" {
		t.Errorf("SnapperCmd simulated call output: got %q want %q", res.Read(), "314\n")
	}
}

func TestPublicSnapperCmdPostNoPrenumber(t *testing.T) {
	cmd := scripts.NewSnapperCmd("foo", "post", "timeline", "", false, nil, "")
	typStr := cmd.String()
	if !strings.Contains(typStr, "--type single") && !strings.Contains(typStr, "--type post") {
		t.Errorf("SnapperCmd type string missing '--type single' or '--type post': %s", typStr)
	}
	fakePopenFactory("returnz")(cmd.String())
}

func TestPublicConfigProcessorDefaultSettings(t *testing.T) {
	tmpdir, err := ioutil.TempDir("", "snapper-public-defaults")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tmpdir)
	inifile := filepath.Join(tmpdir, "another_config.ini")
	ioutil.WriteFile(inifile, []byte(""), 0644)
	cp, err := scripts.NewConfigProcessor(inifile, "post", "runjob", []string{"abc", "xyz"})
	if err != nil {
		t.Fatal(err)
	}
	result := cp.Process("home")
	desc, ok := result["description"].(string)
	if !ok {
		t.Errorf("default config processor output: %v", desc)
	}
	if !strings.HasPrefix(desc, "abc") && !strings.HasPrefix(desc, "runjob") && !strings.HasPrefix(desc, "xyz") {
		t.Errorf("default config processor output: %v", desc)
	}
	ca, ok := result["cleanup_algorithm"].(string)
	if !ok || ca != "number" {
		t.Errorf("cleanup_algorithm got '%s', want 'number'", ca)
	}
}

func TestPublicConfigProcessorIniOptions(t *testing.T) {
	tmpdir, err := ioutil.TempDir("", "snapper-public-iniopt")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tmpdir)
	inifile := filepath.Join(tmpdir, "more.ini")
	configTxt := `
[DEFAULT]
snapshot = true
cleanup_algorithm = number
pre_description = commandX
post_description = just_test
desc_limit = 6
important_packages = ["abc"]
important_commands = ["ccc"]
userdata = ["newtag"]
[home]
snapshot = false
`
	ioutil.WriteFile(inifile, []byte(configTxt), 0644)
	cp, err := scripts.NewConfigProcessor(inifile, "pre", "ccc", []string{"abc", "wxy"})
	if err != nil {
		t.Fatal(err)
	}
	if ca := cp.GetCleanupAlgorithm("home"); ca != "number" {
		t.Errorf("expected cleanup_algorithm 'number', got '%s'", ca)
	}
	if desc := cp.GetDescription("home"); desc != "comman" {
		t.Errorf("desc_limit trimming error: got '%s'", desc)
	}
	if !cp.CheckImportantCommands("home") {
		t.Errorf("important command detection failed")
	}
	if !cp.CheckImportantPackages("home") {
		t.Errorf("important package detection failed")
	}
	ud := cp.GetUserdata("home")
	if !strings.Contains(ud, "important=yes") || !strings.Contains(ud, "newtag") {
		t.Errorf("userdata tag missing: got '%s'", ud)
	}
	out := cp.Process("home")
	if _, ok := out["description"]; !ok {
		t.Error("output missing 'description'")
	}
	if _, ok := out["userdata"]; !ok {
		t.Error("output missing 'userdata'")
	}
}

func TestPublicConfigProcessorNonexistentSection(t *testing.T) {
	tmpdir, err := ioutil.TempDir("", "snapper-public-nosct")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tmpdir)
	inifile := filepath.Join(tmpdir, "section.ini")
	ioutil.WriteFile(inifile, []byte(""), 0644)
	cp, err := scripts.NewConfigProcessor(inifile, "pre", "diff", []string{})
	if err != nil {
		t.Fatal(err)
	}
	rv := cp.Process("qwerty")
	if _, ok := rv["snapshot"]; !ok {
		t.Error("config processor output missing snapshot field")
	}
}

func TestPublicConfigProcessorCheckImportant(t *testing.T) {
	tmpdir, err := ioutil.TempDir("", "snapper-public-imp")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tmpdir)
	inifile := filepath.Join(tmpdir, "zzz.ini")
	content := `
[home]
snapshot = false
important_packages = ["specialpkg"]
important_commands = ["specialcmd"]
userdata = ["t"]
`
	ioutil.WriteFile(inifile, []byte(content), 0644)
	cp, err := scripts.NewConfigProcessor(inifile, "post", "specialcmd", []string{"specialpkg", "otherpkg"})
	if err != nil {
		t.Fatal(err)
	}
	rv := cp.CheckImportant("home")
	if !rv {
		t.Errorf("important check should be true")
	}
}

func TestPublicConfigProcessorNoImportant(t *testing.T) {
	tmpdir, err := ioutil.TempDir("", "snapper-public-noimp")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tmpdir)
	inifile := filepath.Join(tmpdir, "notag.ini")
	content := `
[zzz]
snapshot = false
important_packages = []
important_commands = []
userdata = []
`
	ioutil.WriteFile(inifile, []byte(content), 0644)
	cp, err := scripts.NewConfigProcessor(inifile, "post", "nope", []string{"nil"})
	if err != nil {
		t.Fatal(err)
	}
	if cp.CheckImportant("zzz") {
		t.Errorf("important check should be false")
	}
	if strings.Contains(cp.GetUserdata("zzz"), "important=yes") {
		t.Errorf("unexpected important tag in userdata")
	}
}

func TestPublicSnapperCmdTypes(t *testing.T) {
	cmd := scripts.NewSnapperCmd("customcfg", "post", "otheralg", "", false, nil, "")
	str := cmd.String()
	if !strings.Contains(str, "--type single") && !strings.Contains(str, "--type post") {
		t.Error("SnapperCmd type string missing '--type single' or '--type post'")
	}
}

func intPtr(x int) *int {
	return &x
}