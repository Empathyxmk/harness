package public_tests

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
	"io/ioutil"

	"wesbarnett_snap_pac/scripts"
)

func TestPublicSnapperCmd(t *testing.T) {
	tests := []struct{
		cmd      scripts.SnapperCmd
		expected string
	}{
		{
			scripts.NewSnapperCmd("data", "pre", "timeline", "baz", false, nil, ""),
			`snapper --config data create --cleanup-algorithm timeline --print-number --description "baz" --type pre`,
		},
		{
			scripts.NewSnapperCmd("home", "post", "timeline", "qux", false, intPtr(4321), ""),
			`snapper --config home create --cleanup-algorithm timeline --print-number --description "qux" --pre-number 4321 --type post`,
		},
		{
			scripts.NewSnapperCmd("data", "post", "timeline", "quux", true, intPtr(5678), ""),
			`snapper --no-dbus --config data create --cleanup-algorithm timeline --print-number --description "quux" --pre-number 5678 --type post`,
		},
		{
			scripts.NewSnapperCmd("foo", "post", "timeline", "snap", false, intPtr(8765), "bar=foo"),
			`snapper --config foo create --cleanup-algorithm timeline --print-number --description "snap" --userdata "bar=foo" --pre-number 8765 --type post`,
		},
		{
			scripts.NewSnapperCmd("home", "post", "timeline", "test", false, intPtr(2468), "alpha=beta,gamma=delta"),
			`snapper --config home create --cleanup-algorithm timeline --print-number --description "test" --userdata "alpha=beta,gamma=delta" --pre-number 2468 --type post`,
		},
		{
			scripts.NewSnapperCmd("data", "post", "timeline", "snap", false, nil, "foo=bar,baz=qux"),
			`snapper --config data create --cleanup-algorithm timeline --print-number --description "snap" --userdata "foo=bar,baz=qux" --type single`,
		},
	}
	for i, tst := range tests {
		got := tst.cmd.String()
		if got != tst.expected {
			t.Errorf("case %d: got '%s', want '%s'", i, got, tst.expected)
		}
	}
}

func TestPublicGetSnapperConfigs(t *testing.T) {
	content := `## Path: System/Snapper

## Type:        string
## Default:     ""
# List of snapper configurations.
SNAPPER_CONFIGS="data home alpha beta"
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
	want := []string{"data", "home", "alpha", "beta"}
	if len(got) != len(want) {
		t.Fatalf("got %v, want %v", got, want)
	}
	for i := range got {
		if got[i] != want[i] {
			t.Errorf("index %d: got %s, want %s", i, got[i], want[i])
		}
	}
}

func TestPublicSkipSnapPac(t *testing.T) {
	os.Setenv("SNAP_PAC_SKIP", "yes")
	defer os.Unsetenv("SNAP_PAC_SKIP")
	if !scripts.CheckSkip() {
		t.Error("CheckSkip should return true when SNAP_PAC_SKIP=yes")
	}
}

func TestPublicConfigProcessor(t *testing.T) {
	iniContent := `[home]
important_commands = ["apt-get update"]

cleanup_algorithm = timeline
[beta]
snapshot = True
desc_limit = 5
post_description = test description for beta section
userdata = ["foo=bar", "requestid=99"]

[special]
snapshot = True
cleanup_algorithm = number
important_packages = ["kernel", "initrd"]
userdata = ["foo=bar", "requestid=99"]
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
			args{"home", "bar", []string{"qux"}, "pre"},
			map[string]interface{}{
				"description":      "bar",
				"cleanup_algorithm": "timeline",
				"userdata":         "",
				"snapshot":         true,
			},
		},
		{
			args{"data", "apt-get update", []string{}, "pre"},
			map[string]interface{}{
				"description":      "apt-get update",
				"cleanup_algorithm": "timeline",
				"userdata":         "critical=yes",
				"snapshot":         true,
			},
		},
		{
			args{"archive", "apt-get update", []string{}, "pre"},
			map[string]interface{}{
				"description":      "apt-get update",
				"cleanup_algorithm": "timeline",
				"userdata":         "",
				"snapshot":         false,
			},
		},
		{
			args{"beta", "apt-get update", []string{}, "pre"},
			map[string]interface{}{
				"description":      "apt",
				"cleanup_algorithm": "timeline",
				"userdata":         "foo=bar,requestid=99",
				"snapshot":         true,
			},
		},
		{
			args{"beta", "apt-get update", []string{}, "post"},
			map[string]interface{}{
				"description":      "test d",
				"cleanup_algorithm": "timeline",
				"userdata":         "foo=bar,requestid=99",
				"snapshot":         true,
			},
		},
		{
			args{"special", "apt-get install kernel", []string{"kernel"}, "post"},
			map[string]interface{}{
				"description":      "kernel",
				"cleanup_algorithm": "number",
				"userdata":         "foo=bar,critical=yes,requestid=99",
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

func TestPublicPrefileReadNone(t *testing.T) {
	p := scripts.NewPrefile("data", "pre")
	if p.Read() != "" {
		t.Errorf("expect nil for new prefile")
	}
}

func TestPublicPrefileRead(t *testing.T) {
	p := scripts.NewPrefile("home", "pre")
	p.Write("5678")
	p2 := scripts.NewPrefile("home", "post")
	if content := p2.Read(); content != "5678" {
		t.Errorf("expected prefile content '5678', got '%s'", content)
	}
}

func TestPublicNoPrefile(t *testing.T) {
	p := scripts.NewPrefile("nonexistent-pre-file", "post")
	if out := p.Read(); out != "" {
		t.Errorf("expected nil for non-existent prefile, got '%s'", out)
	}
}

func intPtr(x int) *int {
	return &x
}