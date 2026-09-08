package original

import (
	"os"
	"path/filepath"
	"testing"

	"mherrmann_gitignore_parser"
)

func TestSimple(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("__pycache__/\n*.py[cod]", "/home/michael")
	if matches("/home/michael/main.py") {
		t.Errorf("expected /home/michael/main.py to be NOT ignored")
	}
	if !matches("/home/michael/main.pyc") {
		t.Errorf("expected /home/michael/main.pyc to be ignored")
	}
	if !matches("/home/michael/dir/main.pyc") {
		t.Errorf("expected /home/michael/dir/main.pyc to be ignored")
	}
	if !matches("/home/michael/__pycache__") {
		t.Errorf("expected /home/michael/__pycache__ to be ignored")
	}
}

func TestSimpleParseFile(t *testing.T) {
	// Mock file by creating a temp file
	dir := t.TempDir()
	file := filepath.Join(dir, ".gitignore")
	patterns := "__pycache__/\n*.py[cod]"
	if err := os.WriteFile(file, []byte(patterns), 0644); err != nil {
		t.Fatal(err)
	}

	matches := mherrmann_gitignore_parser.ParseGitignore(file)
	if matches("/home/michael/main.py") {
		t.Errorf("expected /home/michael/main.py to be NOT ignored")
	}
	if !matches("/home/michael/main.pyc") {
		t.Errorf("expected /home/michael/main.pyc to be ignored")
	}
	if !matches("/home/michael/dir/main.pyc") {
		t.Errorf("expected /home/michael/dir/main.pyc to be ignored")
	}
	if !matches("/home/michael/__pycache__") {
		t.Errorf("expected /home/michael/__pycache__ to be ignored")
	}
}

func TestIncompleteFilename(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("o.py", "/home/michael")
	if !matches("/home/michael/o.py") {
		t.Errorf("expected /home/michael/o.py to be ignored")
	}
	if matches("/home/michael/foo.py") {
		t.Errorf("expected /home/michael/foo.py to NOT be ignored")
	}
	if matches("/home/michael/o.pyc") {
		t.Errorf("expected /home/michael/o.pyc to NOT be ignored")
	}
	if !matches("/home/michael/dir/o.py") {
		t.Errorf("expected /home/michael/dir/o.py to be ignored")
	}
	if matches("/home/michael/dir/foo.py") {
		t.Errorf("expected /home/michael/dir/foo.py to NOT be ignored")
	}
	if matches("/home/michael/dir/o.pyc") {
		t.Errorf("expected /home/michael/dir/o.pyc to NOT be ignored")
	}
}

func TestWildcard(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("hello.*", "/home/michael")

	cases := []struct {
		Path   string
		Ignore bool
	}{
		{"/home/michael/hello.txt", true},
		{"/home/michael/hello.foobar/", true},
		{"/home/michael/dir/hello.txt", true},
		{"/home/michael/hello.", true},
		{"/home/michael/hello", false},
		{"/home/michael/helloX", false},
	}
	for _, c := range cases {
		if matches(c.Path) != c.Ignore {
			t.Errorf("with pattern 'hello.*' expected ignore=%v for: %s", c.Ignore, c.Path)
		}
	}
}

func TestAnchoredWildcard(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("/hello.*", "/home/michael")
	if !matches("/home/michael/hello.txt") {
		t.Errorf("/hello.* should match /home/michael/hello.txt")
	}
	if !matches("/home/michael/hello.c") {
		t.Errorf("/hello.* should match /home/michael/hello.c")
	}
	if matches("/home/michael/a/hello.java") {
		t.Errorf("/hello.* should NOT match /home/michael/a/hello.java")
	}
}

func TestTrailingspaces(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr(
		"ignoretrailingspace \n"+
			"notignoredspace\\ \n"+
			"partiallyignoredspace\\  \n"+
			"partiallyignoredspace2 \\  \n"+
			"notignoredmultiplespace\\ \\ \\ ",
		"/home/michael",
	)
	type exstruct struct{ path string; want bool }
	expectations := []exstruct{
		{"/home/michael/ignoretrailingspace", true},
		{"/home/michael/ignoretrailingspace ", false},
		{"/home/michael/partiallyignoredspace ", true},
		{"/home/michael/partiallyignoredspace  ", false},
		{"/home/michael/partiallyignoredspace", false},
		{"/home/michael/partiallyignoredspace2  ", true},
		{"/home/michael/partiallyignoredspace2   ", false},
		{"/home/michael/partiallyignoredspace2 ", false},
		{"/home/michael/partiallyignoredspace2", false},
		{"/home/michael/notignoredspace ", true},
		{"/home/michael/notignoredspace", false},
		{"/home/michael/notignoredmultiplespace   ", true},
		{"/home/michael/notignoredmultiplespace", false},
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
		"somematch\n"+
			"#realcomment\n"+
			"othermatch\n"+
			"\\#imnocomment",
		"/home/michael",
	)
	cases := []struct {
		Path   string
		Ignore bool
	}{
		{"/home/michael/somematch", true},
		{"/home/michael/#realcomment", false},
		{"/home/michael/othermatch", true},
		{"/home/michael/#imnocomment", true},
	}
	for _, c := range cases {
		if matches(c.Path) != c.Ignore {
			t.Errorf("Expected ignore=%v for %s", c.Ignore, c.Path)
		}
	}
}

func TestIgnoreDirectory(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr(".venv/", "/home/michael")
	tests := []struct {
		Path   string
		Ignore bool
	}{
		{"/home/michael/.venv", true},
		{"/home/michael/.venv/folder", true},
		{"/home/michael/.venv/file.txt", true},
		{"/home/michael/.venv_other_folder", false},
		{"/home/michael/.venv_no_folder.py", false},
	}
	for _, c := range tests {
		if matches(c.Path) != c.Ignore {
			t.Errorf("Expected ignore=%v for %s", c.Ignore, c.Path)
		}
	}
}

func TestIgnoreDirectoryAsterisk(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr(".venv/*", "/home/michael")
	tests := []struct {
		Path   string
		Ignore bool
	}{
		{"/home/michael/.venv", false},
		{"/home/michael/.venv/folder", true},
		{"/home/michael/.venv/file.txt", true},
	}
	for _, c := range tests {
		if matches(c.Path) != c.Ignore {
			t.Errorf("Expected ignore=%v for %s", c.Ignore, c.Path)
		}
	}
}

func TestNegation(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr(
		"*.ignore\n!keep.ignore", "/home/michael",
	)
	if !matches("/home/michael/trash.ignore") {
		t.Errorf("trash.ignore: expect ignore")
	}
	if matches("/home/michael/keep.ignore") {
		t.Errorf("keep.ignore: expect NOT ignore")
	}
	if !matches("/home/michael/waste.ignore") {
		t.Errorf("waste.ignore: expect ignore")
	}
}

func TestLiteralExclamationMark(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("\\!ignore_me!", "/home/michael")
	if !matches("/home/michael/!ignore_me!") {
		t.Errorf("should ignore /home/michael/!ignore_me!")
	}
	if matches("/home/michael/ignore_me!") {
		t.Errorf("should NOT ignore /home/michael/ignore_me!")
	}
	if matches("/home/michael/ignore_me") {
		t.Errorf("should NOT ignore /home/michael/ignore_me")
	}
}

func TestDoubleAsterisks(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("foo/**/Bar", "/home/michael")
	if !matches("/home/michael/foo/hello/Bar") {
		t.Errorf("should match /home/michael/foo/hello/Bar")
	}
	if !matches("/home/michael/foo/world/Bar") {
		t.Errorf("should match /home/michael/foo/world/Bar")
	}
	if !matches("/home/michael/foo/Bar") {
		t.Errorf("should match /home/michael/foo/Bar")
	}
	if matches("/home/michael/foo/BarBar") {
		t.Errorf("should not match /home/michael/foo/BarBar")
	}
}

func TestDoubleAsteriskNoSlashesSingleAsterisk(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("a/b**c/d", "/home/michael")
	tests := []struct {
		Path   string
		Ignore bool
	}{
		{"/home/michael/a/bc/d", true},
		{"/home/michael/a/bXc/d", true},
		{"/home/michael/a/bbc/d", true},
		{"/home/michael/a/bcc/d", true},
		{"/home/michael/a/bcd", false},
		{"/home/michael/a/b/c/d", false},
		{"/home/michael/a/bb/cc/d", false},
		{"/home/michael/a/bb/XX/cc/d", false},
	}
	for _, c := range tests {
		if matches(c.Path) != c.Ignore {
			t.Errorf("Expected ignore=%v for %s", c.Ignore, c.Path)
		}
	}
}

func TestMoreAsterisksLikeSingleAsterisk(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("***a/b", "/home/michael")
	if !matches("/home/michael/XYZa/b") {
		t.Errorf("XYZa/b should be ignored")
	}
	if matches("/home/michael/foo/a/b") {
		t.Errorf("foo/a/b should NOT be ignored")
	}

	matches2 := mherrmann_gitignore_parser.ParseGitignoreStr("a/b***", "/home/michael")
	if !matches2("/home/michael/a/bXYZ") {
		t.Errorf("a/bXYZ should be ignored")
	}
	if matches2("/home/michael/a/b/foo") {
		t.Errorf("a/b/foo should NOT be ignored")
	}
}

func TestDirectoryOnlyNegation(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr(
		"data/**\n!data/**/\n!.gitkeep\n!data/01_raw/*",
		"/home/michael",
	)
	tests := []struct {
		Path   string
		Ignore bool
	}{
		{"/home/michael/data/01_raw/", false},
		{"/home/michael/data/01_raw/.gitkeep", false},
		{"/home/michael/data/01_raw/raw_file.csv", false},
		{"/home/michael/data/02_processed/", false},
		{"/home/michael/data/02_processed/.gitkeep", false},
		{"/home/michael/data/02_processed/processed_file.csv", true},
	}
	for _, c := range tests {
		if matches(c.Path) != c.Ignore {
			t.Errorf("Expected ignore=%v for %s", c.Ignore, c.Path)
		}
	}
}

func TestSingleAsterisk(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("*", "/home/michael")
	tests := []struct {
		Path   string
		Ignore bool
	}{
		{"/home/michael/file.txt", true},
		{"/home/michael/directory", true},
		{"/home/michael/directory-trailing/", true},
	}
	for _, c := range tests {
		if matches(c.Path) != c.Ignore {
			t.Errorf("Expected ignore=%v for %s", c.Ignore, c.Path)
		}
	}
}

func TestSupportsPathTypeArgument(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("file1\n!file2", "/home/michael")
	if !matches("/home/michael/file1") {
		t.Errorf("/home/michael/file1 should be ignored")
	}
	if matches("/home/michael/file2") {
		t.Errorf("/home/michael/file2 should NOT be ignored")
	}
}

func TestSlashInRangeDoesNotMatchDirs(t *testing.T) {
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("abc[X-Z/]def", "/home/michael")
	if matches("/home/michael/abcdef") {
		t.Errorf("Should not ignore /home/michael/abcdef")
	}
	if !matches("/home/michael/abcXdef") || !matches("/home/michael/abcYdef") || !matches("/home/michael/abcZdef") {
		t.Errorf("abcXdef, abcYdef, abcZdef should be ignored")
	}
	if matches("/home/michael/abc/def") {
		t.Errorf("abc/def should NOT be ignored")
	}
	if matches("/home/michael/abcXYZdef") {
		t.Errorf("abcXYZdef should NOT be ignored")
	}
}

func TestSymlinkToAnotherDirectory(t *testing.T) {
	projDir := t.TempDir()
	otherDir := t.TempDir()
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("link", projDir)

	link := filepath.Join(projDir, "link")
	target := filepath.Join(otherDir, "target")
	if err := os.Symlink(target, link); err != nil {
		t.Fatalf("could not create symlink: %v", err)
	}
	// Symbolic links are not followed, match as regular files
	if !matches(link) {
		t.Errorf("symlink should be matched as file")
	}
}

func TestSymlinkToSymlinkDirectory(t *testing.T) {
	projDir := t.TempDir()
	linkDir := t.TempDir()
	link := filepath.Join(linkDir, "link")
	if err := os.Symlink(projDir, link); err != nil {
		t.Fatalf("setup: could not create symlink: %v", err)
	}
	file := filepath.Join(link, "file.txt")
	matches := mherrmann_gitignore_parser.ParseGitignoreStr("file.txt", linkDir)
	if !matches(file) {
		t.Errorf("file.txt under symlink directory should be ignored")
	}
}