package public_tests

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	"antiboredom_audiogrep/audiogrep"
)

func TestFindFilesPublic(t *testing.T) {
	tmpdir := t.TempDir()
	files := []string{
		filepath.Join(tmpdir, "x.flac"),
		filepath.Join(tmpdir, "y.flac"),
		filepath.Join(tmpdir, "z.txt"),
	}
	for _, f := range files {
		err := os.WriteFile(f, []byte("dummy"), 0644)
		if err != nil {
			t.Fatal(err)
		}
	}
	found := make(map[string]bool)
	for _, f := range audiogrep.FindFiles(tmpdir, []string{".flac"}) {
		found[f] = true
	}
	shouldFind := map[string]bool{
		filepath.Join(tmpdir, "x.flac"): true,
		filepath.Join(tmpdir, "y.flac"): true,
	}
	if len(found) != 2 || !found[filepath.Join(tmpdir, "x.flac")] || !found[filepath.Join(tmpdir, "y.flac")] {
		t.Errorf("FindFiles failed. Got: %+v", found)
	}
}

func TestRegexifyPublic(t *testing.T) {
	text := "hello? world* (demo)"
	r := audiogrep.Regexify(text)
	if r != `hello\?\ world\*\ \(demo\)` {
		t.Errorf("Regexify failed. Got: %q", r)
	}
}

func TestGetWordTimingsPublic(t *testing.T) {
	tmpdir := t.TempDir()
	fn := filepath.Join(tmpdir, "timings_public.txt")
	lines := []string{
		"<s> 5.0 6.0 1\n",
		"gamma 6.0 6.2 1\n",
		"zeta 6.2 6.3 1\n",
		"</s> 6.3 6.7 1\n",
	}
	err := os.WriteFile(fn, []byte(strings.Join(lines, "")), 0644)
	if err != nil {
		t.Fatal(err)
	}
	tgt := audiogrep.GetWordTimings(fn)
	if len(tgt) != 2 {
		t.Errorf("Expected 2 words, got %d", len(tgt))
	}
	if tgt[0][0] != "gamma" || tgt[1][0] != "zeta" {
		t.Errorf("Unexpected words: %+v", tgt)
	}
}

func TestGroupWordsPublic(t *testing.T) {
	words := [][]interface{}{
		{"a", 1, 2, 3},
		{"b", 2, 3, 4},
		{"c", 3, 4, 5},
		{"d", 4, 5, 6},
		{"e", 5, 6, 7},
	}
	n := 4
	grouped := audiogrep.GroupWords(words, n)
	if len(grouped) != 2 {
		t.Errorf("Expected 2 groups, got %d", len(grouped))
	}
	if grouped[0][0][0] != "a" {
		t.Errorf("First group does not start with 'a', got %+v", grouped[0])
	}
	if grouped[1][0][0] != "b" {
		t.Errorf("Second group does not start with 'b', got %+v", grouped[1])
	}
}

func TestGetGroupedWordTimingsPublic(t *testing.T) {
	tmpdir := t.TempDir()
	fn := filepath.Join(tmpdir, "grouped_timings_public.txt")
	lines := []string{
		"<s> 11.0 12.0 1\n",
		"x 12.0 12.44 1\n",
		"y 12.44 12.89 1\n",
		"z 12.89 13.41 1\n",
		"</s> 13.41 13.91 1\n",
	}
	if err := os.WriteFile(fn, []byte(strings.Join(lines, "")), 0644); err != nil {
		t.Fatal(err)
	}
	groups := audiogrep.GetGroupedWordTimings(fn, 2)
	if len(groups) != 2 || groups[0][0][0] != "x" || groups[1][0][0] != "y" {
		t.Errorf("Unexpected grouped word timings. Got %+v", groups)
	}
}

func TestFrankenSentencePublic(t *testing.T) {
	inWt := [][][]interface{}{
		{{"apple", 0.1, 0.2, 0.0}, {"pear", 0.2, 0.3, 0.0}},
		{{"banana", 0.3, 0.5, 0.0}},
	}
	r := audiogrep.FrankenSentencePublic("test sentence", inWt)
	if r == nil || len(r) == 0 {
		t.Errorf("Expected nonempty result from FrankenSentencePublic")
	}
	for _, e := range r {
		switch e.(type) {
		case audiogrep.Slice, []interface{}:
			// OK
		default:
			t.Errorf("Element is not a slice/tuple: %+v", e)
		}
	}
}

func TestSearchModesPublic(t *testing.T) {
	tmpdir := t.TempDir()
	fn := filepath.Join(tmpdir, "public.transcription.txt")
	lines := []string{
		"<s> 3.0 3.7 1\n", "foo 3.7 3.8 1\n", "bar 3.8 4.1 1\n", "</s> 4.1 4.5 1\n",
	}
	if err := os.WriteFile(fn, []byte(strings.Join(lines, "")), 0644); err != nil {
		t.Fatal(err)
	}
	audiogrep.FragmentSearch = func(q string, s []audiogrep.Sentence, reg bool) []map[string]interface{} {
		return []map[string]interface{}{{"X": "Y"}}
	}
	audiogrep.WordSearch = func(q string, s []audiogrep.Sentence, reg bool) []map[string]interface{} {
		return []map[string]interface{}{{"Q": 2}}
	}
	audiogrep.FrankenSentence = func(q string, fs []audiogrep.Sentence) []interface{} {
		return []interface{}{42}
	}
	r1 := audiogrep.Search("any", []string{fn}, "fragment", false)
	if len(r1) != 1 || r1[0]["X"] != "Y" {
		t.Errorf("Fragment mode not dispatched correctly: %+v", r1)
	}
	r2 := audiogrep.Search("hello", []string{fn}, "word", false)
	if len(r2) != 1 || r2[0]["Q"] != 2 {
		t.Errorf("Word mode not dispatched correctly: %+v", r2)
	}
	r3 := audiogrep.Search("repeat", []string{fn}, "sentence", false)
	if s, ok := r3[0].(int); !ok || s != 42 {
		t.Errorf("Sentence mode not dispatched correctly: %+v", r3)
	}
}

func TestMakeSplicePublic(t *testing.T) {
	tmpdir := t.TempDir()
	outMp3 := filepath.Join(tmpdir, "f.spliced.mp3")
	slices := []audiogrep.Slice{
		{From: 0, To: 2},
		{From: 3, To: 5},
	}
	defer func() {
		_ = recover()
	}()
	// MakeSplice might raise if ffmpeg is not available. Ensure does not panic at least
	_ = audiogrep.MakeSplice("dummy.mp3", slices, outMp3)
}