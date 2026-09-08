package tests

import (
	"os"
	"testing"
)

type UtilObj struct{}

func (u UtilObj) Cwd(path string, fn func()) {
	cur, _ := os.Getwd()
	os.Chdir(path)
	defer os.Chdir(cur)
	fn()
}

func TestChCwd(t *testing.T) {
	origDir, _ := os.Getwd()
	tmp := os.TempDir()
	utils := UtilObj{}
	utils.Cwd(tmp, func() {
		cur, _ := os.Getwd()
		if cur != tmp {
			t.Error("tempdir not chdir")
		}
	})
	cur, _ := os.Getwd()
	if cur != origDir {
		t.Error("cwd not restored")
	}
}