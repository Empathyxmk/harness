package public_tests

import (
	"os"
	"path/filepath"
	"testing"
	"mherrmann_gitignore_parser"
)

func TestSimple(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("build/\n*.log", "/example")
	if matches("/example/main.txt") {
		t.Errorf("expected /example/main.txt NOT to be ignored")
	}
	if !matches("/example/main.log") {
		t.Errorf("expected /example/main.log to be ignored")
	}
	if !matches("/example/dir/main.log") {
		t.Errorf("expected /example/dir/main.log to be ignored")
	}
	if !matches("/example/build") {
		t.Errorf("expected /example/build to be ignored")
	}
}

func TestSimpleParseFile(t *testing.T) {
	dir := t.TempDir()
	file := filepath.Join(dir, ".gitignore")
	if err := os.WriteFile(file, []byte("dist/\n*.tmp"), 0644); err != nil {
		t.Fatal(err)
	}

	matches := mherrmann_gitignore_parser.ParseGitignore(file)
	if matches("/project/app.py") {
		t.Errorf("expected /project/app.py NOT to be ignored")
	}
	if !matches("/project/app.tmp") {
		t.Errorf("expected /project/app.tmp to be ignored")
	}
	if !matches("/project/sub/app.tmp") {
		t.Errorf("expected /project/sub/app.tmp to be ignored")
	}
	if !matches("/project/dist") {
		t.Errorf("expected /project/dist to be ignored")
	}
}

func TestIncompleteFilename(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("app.js", "/public")
	cases := []struct {
		Path   string
		Ignore bool
	}{
		{"/public/app.js", true},
		{"/public/test.js", false},
		{"/public/app.jsx", false},
		{"/public/dir/app.js", true},
		{"/public/dir/test.js", false},
		{"/public/dir/app.jsx", false},
	}
	for _, c := range cases {
		if matches(c.Path) != c.Ignore {
			t.Errorf("expected ignore=%v for path %s", c.Ignore, c.Path)
		}
	}
}

func TestWildcard(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("error.*", "/tmp")
	tests := []struct {
		Path   string
		Ignore bool
	}{
		{"/tmp/error.txt", true},
		{"/tmp/error.bak/", true},
		{"/tmp/dir/error.txt", true},
		{"/tmp/error.", true},
		{"/tmp/error", false},
		{"/tmp/errorX", false},
	}
	for _, tt := range tests {
		if matches(tt.Path) != tt.Ignore {
			t.Errorf("expected ignore=%v for %s", tt.Ignore, tt.Path)
		}
	}
}

func TestAnchoredWildcard(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("/success.*", "/dirfoo")
	if !matches("/dirfoo/success.txt") {
		t.Errorf("should ignore /dirfoo/success.txt")
	}
	if !matches("/dirfoo/success.c") {
		t.Errorf("should ignore /dirfoo/success.c")
	}
	if matches("/dirfoo/a/success.java") {
		t.Errorf("should NOT ignore /dirfoo/a/success.java")
	}
}

func TestTrailingSpaces(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr(
		"ignoretailspace \n"+
			"notignoredspace\\ \n"+
			"almostignoredspace\\  \n"+
			"almostignoredspace2 \\  \n"+
			"notignoredmultiplespace\\ \\ \\ ",
		"/abc",
	)
	type exp struct{ path string; want bool }
	expectations := []exp{
		{"/abc/ignoretailspace", true},
		{"/abc/ignoretailspace ", false},
		{"/abc/almostignoredspace ", true},
		{"/abc/almostignoredspace  ", false},
		{"/abc/almostignoredspace", false},
		{"/abc/almostignoredspace2  ", true},
		{"/abc/almostignoredspace2   ", false},
		{"/abc/almostignoredspace2 ", false},
		{"/abc/almostignoredspace2", false},
		{"/abc/notignoredspace ", true},
		{"/abc/notignoredspace", false},
		{"/abc/notignoredmultiplespace   ", true},
		{"/abc/notignoredmultiplespace", false},
	}
	for _, e := range expectations {
		got := matches(e.path)
		if got != e.want {
			t.Errorf("Expected ignore=%v for %s", e.want, e.path)
		}
	}
}

func TestComment(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr(
		"firstmatch\n"+
			"#notrealcomment\n"+
			"secondmatch\n"+
			"\\#reallyamatch",
		"/bdir",
	)
	cases := []struct {
		Path   string
		Ignore bool
	}{
		{"/bdir/firstmatch", true},
		{"/bdir/#notrealcomment", false},
		{"/bdir/secondmatch", true},
		{"/bdir/#reallyamatch", true},
	}
	for _, c := range cases {
		if matches(c.Path) != c.Ignore {
			t.Errorf("Expected ignore=%v for %s", c.Ignore, c.Path)
		}
	}
}

func TestIgnoreDirectory(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("cache/", "/mnt")
	cases := []struct {
		Path   string
		Ignore bool
	}{
		{"/mnt/cache", true},
		{"/mnt/cache/subdir", true},
		{"/mnt/cache/file.txt", true},
		{"/mnt/cachex", false},
		{"/mnt/cache_v2.py", false},
	}
	for _, c := range cases {
		if matches(c.Path) != c.Ignore {
			t.Errorf("expected ignore=%v for %s", c.Ignore, c.Path)
		}
	}
}

func TestIgnoreDirectoryAsterisk(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("output/*", "/results")
	tests := []struct {
		Path   string
		Ignore bool
	}{
		{"/results/output", false},
		{"/results/output/folder", true},
		{"/results/output/file.txt", true},
	}
	for _, c := range tests {
		if matches(c.Path) != c.Ignore {
			t.Errorf("expected ignore=%v for %s", c.Ignore, c.Path)
		}
	}
}

func TestNegation(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("*.bak\n!keep.bak", "/store")
	cases := []struct {
		Path   string
		Ignore bool
	}{
		{"/store/junk.bak", true},
		{"/store/keep.bak", false},
		{"/store/lost.bak", true},
	}
	for _, c := range cases {
		if matches(c.Path) != c.Ignore {
			t.Errorf("expected ignore=%v for %s", c.Ignore, c.Path)
		}
	}
}

func TestLiteralExclamationMark(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("\\!saveit!", "/fs")
	if !matches("/fs/!saveit!") {
		t.Errorf("should ignore /fs/!saveit!")
	}
	if matches("/fs/saveit!") {
		t.Errorf("should NOT ignore /fs/saveit!")
	}
	if matches("/fs/saveit") {
		t.Errorf("should NOT ignore /fs/saveit")
	}
}

func TestDoubleAsterisks(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("dir/**/Final", "/abc")
	cases := []struct {
		Path   string
		Ignore bool
	}{
		{"/abc/dir/sub/Final", true},
		{"/abc/dir/foo/Final", true},
		{"/abc/dir/Final", true},
		{"/abc/dir/Finals", false},
	}
	for _, c := range cases {
		if matches(c.Path) != c.Ignore {
			t.Errorf("expected ignore=%v for %s", c.Ignore, c.Path)
		}
	}
}

func TestDoubleAsteriskWithoutSlashesHandledLikeSingleAsterisk(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("m/n**o/p", "/usr")
	cases := []struct {
		Path   string
		Ignore bool
	}{
		{"/usr/m/no/p", true},
		{"/usr/m/nko/p", true},
		{"/usr/m/nno/p", true},
		{"/usr/m/noo/p", true},
		{"/usr/m/nop", false},
		{"/usr/m/n/o/p", false},
		{"/usr/m/nn/oo/p", false},
		{"/usr/m/nn/YY/oo/p", false},
	}
	for _, c := range cases {
		if matches(c.Path) != c.Ignore {
			t.Errorf("expected ignore=%v for %s", c.Ignore, c.Path)
		}
	}
}

func TestMoreAsterisksHandledLikeSingleAsterisk(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("***z/x", "/sample")
	if !matches("/sample/ABCz/x") {
		t.Errorf("should ignore /sample/ABCz/x")
	}
	if matches("/sample/yyy/z/x") {
		t.Errorf("should NOT ignore /sample/yyy/z/x")
	}
	matches2 := mherrmann_gitignore_parser.ParseGitignoreStr("z/x***", "/sample")
	if !matches2("/sample/z/xABC") {
		t.Errorf("should ignore /sample/z/xABC")
	}
	if matches2("/sample/z/x/abc") {
		t.Errorf("should NOT ignore /sample/z/x/abc")
	}
}

func TestDirectoryOnlyNegation(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr(
		"content/**\n!content/**/\n!.hold\n!content/01_data/*", "/vault",
	)
	tests := []struct {
		Path   string
		Ignore bool
	}{
		{"/vault/content/01_data/", false},
		{"/vault/content/01_data/.hold", false},
		{"/vault/content/01_data/doc.csv", false},
		{"/vault/content/02_final/", false},
		{"/vault/content/02_final/.hold", false},
		{"/vault/content/02_final/summary.txt", true},
	}
	for _, c := range tests {
		if matches(c.Path) != c.Ignore {
			t.Errorf("expected ignore=%v for %s", c.Ignore, c.Path)
		}
	}
}

func TestSingleAsterisk(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("*", "/misc")
	cases := []struct {
		Path   string
		Ignore bool
	}{
		{"/misc/note.txt", true},
		{"/misc/folder", true},
		{"/misc/folder-trailing/", true},
	}
	for _, c := range cases {
		if matches(c.Path) != c.Ignore {
			t.Errorf("expected ignore=%v for %s", c.Ignore, c.Path)
		}
	}
}

func TestSupportsPathTypeArgument(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("image1\n!image2", "/photos")
	if !matches("/photos/image1") {
		t.Errorf("/photos/image1 should be ignored")
	}
	if matches("/photos/image2") {
		t.Errorf("/photos/image2 should NOT be ignored")
	}
}

func TestSlashInRangeDoesNotMatchDirs(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("pqr[S-U/]stu", "/zdir")
	cases := []struct {
		Path   string
		Ignore bool
	}{
		{"/zdir/pqrststu", false},
		{"/zdir/pqrSstu", true},
		{"/zdir/pqrTstu", true},
		{"/zdir/pqrUstu", true},
		{"/zdir/pqr/stu", false},
		{"/zdir/pqrSTUstu", false},
	}
	for _, c := range cases {
		if matches(c.Path) != c.Ignore {
			t.Errorf("expected ignore=%v for %s", c.Ignore, c.Path)
		}
	}
}

func TestSymlinkToAnotherDirectory(t *testing.T) {
	rootDir := t.TempDir()
	otherDir := t.TempDir()
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("linker", rootDir)
	linkerPath := filepath.Join(rootDir, "linker")
	if err := os.Symlink(otherDir, linkerPath); err != nil {
		t.Fatalf("could not create symlink: %v", err)
	}
	if !matches(linkerPath) {
		t.Errorf("symlink should be ignored as file")
	}
	if matches(filepath.Join(rootDir, "link")) {
		t.Errorf("should not ignore unrelated link")
	}
}