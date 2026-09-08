package original

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
	"io/ioutil"

	"wesbarnett_snap_pac/scripts"
)

func TestSnapperCmd(t *testing.T) {
	tests := []struct{
		cmd      scripts.SnapperCmd
		expected string
	}{
		{
			scripts.NewSnapperCmd("root", "pre", "number", "foo", false, nil, ""),
			`snapper --config root create --cleanup-algorithm number --print-number --description "foo" --type pre`,
		},
		{
			scripts.NewSnapperCmd("root", "post", "number", "bar", false, intPtr(1234), ""),
			`snapper --config root create --cleanup-algorithm number --print-number --description "bar" --pre-number 1234 --type post`,
		},
		{
			scripts.NewSnapperCmd("root", "post", "number", "bar", true, intPtr(1234), ""),
			`snapper --no-dbus --config root create --cleanup-algorithm number --print-number --description "bar" --pre-number 1234 --type post`,
		},
		{
			scripts.NewSnapperCmd("root", "post", "number", "bar", false, intPtr(1234), "important=yes"),
			`snapper --config root create --cleanup-algorithm number --print-number --description "bar" --userdata "important=yes" --pre-number 1234 --type post`,
		},
		{
			scripts.NewSnapperCmd("root", "post", "number", "bar", false, intPtr(1234), "foo=bar,important=yes"),
			`snapper --config root create --cleanup-algorithm number --print-number --description "bar" --userdata "foo=bar,important=yes" --pre-number 1234 --type post`,
		},
		{
			scripts.NewSnapperCmd("root", "post", "number", "bar", false, nil, "foo=bar,important=yes"),
			`snapper --config root create --cleanup-algorithm number --print-number --description "bar" --userdata "foo=bar,important=yes" --type single`,
		},
	}
	for i, tst := range tests {
		got := tst.cmd.String()
		if got != tst.expected {
			t.Errorf("case %d: got '%s', want '%s'", i, got, tst.expected)
		}
	}
}

func TestGetSnapperConfigs(t *testing.T) {
	content := `## Path: System/Snapper

## Type:        string
## Default:     ""
# List of snapper configurations.
SNAPPER_CONFIGS="home root foo bar"
`
	tmpfile, err := ioutil.TempFile("", "snapperconfig")
	if err != nil {
		t.Fatal(err)
	}
	defer os.Remove(tmpfile.Name())
	if _, err := tmpfile.Write([]byte(content)); err != nil {
		t.Fatal(err)
	}
	tmpfile.Close()

	got := scripts.GetSnapperConfigs(tmpfile.Name())
	want := []string{"home", "root", "foo", "bar"}
	if len(got) != len(want) {
		t.Fatalf("got %v, want %v", got, want)
	}
	for i := range got {
		if got[i] != want[i] {
			t.Errorf("index %d: got %s, want %s", i, got[i], want[i])
		}
	}
}

func TestSkipSnapPac(t *testing.T) {
	os.Setenv("SNAP_PAC_SKIP", "y")
	defer os.Unsetenv("SNAP_PAC_SKIP")
	if !scripts.CheckSkip() {
		t.Error("CheckSkip should return true when SNAP_PAC_SKIP=y")
	}
}

func TestConfigProcessor(t *testing.T) {
	iniContent := `[root]
important_commands = ["pacman -Syu"]

[home]
snapshot = True
desc_limit = 3
post_description = a really long description
userdata = ["foo=bar", "requestid=42"]

[myconfig]
snapshot = True
cleanup_algorithm = timeline
important_packages = ["linux", "linux-lts"]
userdata = ["foo=bar", "requestid=42"]
`
	tmpfile, err := ioutil.TempFile("", "snapperconfig-*.ini")
	if err != nil {
		t.Fatal(err)
	}
	defer os.Remove(tmpfile.Name())
	if _, err := tmpfile.Write([]byte(iniContent)); err != nil {
		t.Fatal(err)
	}
	tmpfile.Close()

	type args struct {
		section       string
		command       string
		packages      []string
		snapshot_type string
	}
	tests := []struct {
		a      args
		result map[string]interface{}
	}{
		{
			args{"root", "foo", []string{"bar"}, "pre"},
			map[string]interface{}{
				"description":      "foo",
				"cleanup_algorithm": "number",
				"userdata":         "",
				"snapshot":         true,
			},
		},
		{
			args{"root", "pacman -Syu", []string{}, "pre"},
			map[string]interface{}{
				"description":      "pacman -Syu",
				"cleanup_algorithm": "number",
				"userdata":         "important=yes",
				"snapshot":         true,
			},
		},
		{
			args{"mail", "pacman -Syu", []string{}, "pre"},
			map[string]interface{}{
				"description":      "pacman -Syu",
				"cleanup_algorithm": "number",
				"userdata":         "",
				"snapshot":         false,
			},
		},
		{
			args{"home", "pacman -Syu", []string{}, "pre"},
			map[string]interface{}{
				"description":      "pac",
				"cleanup_algorithm": "number",
				"userdata":         "foo=bar,requestid=42",
				"snapshot":         true,
			},
		},
		{
			args{"home", "pacman -Syu", []string{}, "post"},
			map[string]interface{}{
				"description":      "a r",
				"cleanup_algorithm": "number",
				"userdata":         "foo=bar,requestid=42",
				"snapshot":         true,
			},
		},
		{
			args{"myconfig", "pacman -S linux", []string{"linux"}, "post"},
			map[string]interface{}{
				"description":      "linux",
				"cleanup_algorithm": "timeline",
				"userdata":         "foo=bar,important=yes,requestid=42",
				"snapshot":         true,
			},
		},
	}
	for i, tst := range tests {
		cp, err := scripts.NewConfigProcessor(tmpfile.Name(), tst.a.snapshot_type, tst.a.command, tst.a.packages)
		if err != nil {
			t.Fatalf("case %d: failed to create ConfigProcessor: %v", i, err)
		}
		got := cp.Process(tst.a.section)
		for k, wantVal := range tst.result {
			gotVal, ok := got[k]
			if !ok {
				t.Errorf("case %d: missing expected key %s", i, k)
				continue
			}
			// For strict equality
			if gotVal != wantVal {
				t.Errorf("case %d: key %s: got %v want %v", i, k, gotVal, wantVal)
			}
		}
	}
}

func TestPrefileReadNone(t *testing.T) {
	p := scripts.NewPrefile("root", "pre")
	if p.Read() != "" {
		t.Errorf("expect nil for new prefile")
	}
}

func TestPrefileRead(t *testing.T) {
	p := scripts.NewPrefile("root", "pre")
	p.Write("1234")
	p2 := scripts.NewPrefile("root", "post")
	if content := p2.Read(); content != "1234" {
		t.Errorf("expected prefile content '1234', got '%s'", content)
	}
}

func TestNoPrefile(t *testing.T) {
	p := scripts.NewPrefile("foo-pre-file-not-found", "post")
	if out := p.Read(); out != "" {
		t.Errorf("expected nil for non-existent prefile, got '%s'", out)
	}
}

func intPtr(x int) *int {
	return &x
}