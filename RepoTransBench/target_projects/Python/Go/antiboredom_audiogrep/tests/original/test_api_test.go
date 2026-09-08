package original

import (
	"bytes"
	"errors"
	"io/ioutil"
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"testing"

	"antiboredom_audiogrep/audiogrep"
)

// Helper: simulate monkeypatch by swapping out functions in audiogrep.
// Go doesn't have dynamic patching; use interface-based/test funcs.

func TestConvertToWavCallsSubprocess(t *testing.T) {
	tmpdir := t.TempDir()
	testFile := filepath.Join(tmpdir, "audio.mp3")
	err := ioutil.WriteFile(testFile, []byte("abc"), 0644)
	if err != nil {
		t.Fatal(err)
	}
	called := false

	origSubprocessCall := audiogrep.SubprocessCall
	origPathExists := audiogrep.PathExists
	defer func() {
		audiogrep.SubprocessCall = origSubprocessCall
		audiogrep.PathExists = origPathExists
	}()

	audiogrep.SubprocessCall = func(args []string) error {
		called = true
		outFile := testFile + ".temp.wav"
		_ = ioutil.WriteFile(outFile, []byte("dummy"), 0644)
		return nil
	}
	audiogrep.PathExists = func(f string) bool { return false }

	out, err := audiogrep.ConvertToWav([]string{testFile})
	if err != nil {
		t.Fatalf("ConvertToWav error: %v", err)
	}
	if len(out) != 1 || out[0] != testFile+".temp.wav" {
		t.Errorf("unexpected wav output: %v", out)
	}
	if !called {
		t.Error("SubprocessCall was not called when expected")
	}

	// Now set path exists = true, should NOT call subprocess
	called = false
	audiogrep.PathExists = func(f string) bool { return true }
	out2, err := audiogrep.ConvertToWav([]string{testFile})
	if err != nil {
		t.Fatalf("ConvertToWav error: %v", err)
	}
	if len(out2) != 1 || out2[0] != testFile+".temp.wav" {
		t.Errorf("unexpected wav output: %v", out2)
	}
	if called {
		t.Error("SubprocessCall should not run if output already exists")
	}
}

func TestWordsJSONValidAndInvalid(t *testing.T) {
	s := []map[string]interface{}{
		{"words": [][]string{{"hello", "1", "2", "0.5"}, {"world", "2", "3", "0.8"}}, "file": "foo"},
	}
	j, err := audiogrep.WordsJSON(s)
	if err != nil {
		t.Fatalf("WordsJSON failed: %v", err)
	}
	if !strings.Contains(j, `"word": "hello"`) {
		t.Errorf("Output JSON did not contain required word, got: %v", j)
	}

	// Should not panic on invalid structure
	s2 := []map[string]interface{}{
		{"words": [][]string{{"x", "y"}}, "file": "foo"},
	}
	_, _ = audiogrep.WordsJSON(s2)
	// (no panic), success
}

func TestConvertTimestampsEdgeCases(t *testing.T) {
	sentences, err := audiogrep.ConvertTimestamps([]string{"/not/a/file"})
	if err != nil {
		t.Fatalf("ConvertTimestamps should not error: %v", err)
	}
	if len(sentences) != 0 {
		t.Errorf("Expected empty on missing file, got: %v", sentences)
	}
	tmpdir := t.TempDir()
	fileName := filepath.Join(tmpdir, "nofile.mp3")
	sentences2, err := audiogrep.ConvertTimestamps([]string{fileName})
	if err != nil {
		t.Fatalf("ConvertTimestamps should not error: %v", err)
	}
	if len(sentences2) != 0 {
		t.Errorf("Expected empty on missing file, got: %v", sentences2)
	}
}

func TestConvertTimestampsSentence(t *testing.T) {
	tmpdir := t.TempDir()
	fn := filepath.Join(tmpdir, "x.transcription.txt")
	lines := []string{
		"<s> 0.0 0.2 1.0\n", "word 0.2 0.3 1.0\n", "</s> 0.3 0.5 1.0\n",
	}
	err := ioutil.WriteFile(fn, []byte(strings.Join(lines, "")), 0644)
	if err != nil {
		t.Fatal(err)
	}
	sents, err := audiogrep.ConvertTimestamps([]string{fn})
	if err != nil {
		t.Fatalf("ConvertTimestamps error: %v", err)
	}
	if len(sents) == 0 {
		t.Fatalf("No sentences found")
	}
	sent := sents[0]
	if sent.Start != 0.0 || sent.End != 0.3 {
		t.Errorf("Unexpected sentence start/end: %+v", sent)
	}
	if len(sent.Words) != 1 {
		t.Errorf("Expected 1 word got %d", len(sent.Words))
	}
	if sent.Words[0][0] != "word" {
		t.Errorf("Got wrong word: %+v", sent.Words[0][0])
	}
}

func TestTextReadsSentences(t *testing.T) {
	tmpdir := t.TempDir()
	fn := filepath.Join(tmpdir, "test.transcription.txt")
	lines := []string{
		"<s> 1 2 1\n", "a 2 3 1\n", "b 4 5 1\n", "</s> 6 7 1\n",
	}
	err := ioutil.WriteFile(fn, []byte(strings.Join(lines, "")), 0644)
	if err != nil {
		t.Fatal(err)
	}
	res, err := audiogrep.Text([]string{fn})
	if err != nil {
		t.Fatal(err)
	}
	if !strings.Contains(res, "a b") {
		t.Errorf("Expected 'a b' in result, got: %v", res)
	}
}

func TestTranscribeRuns(t *testing.T) {
	tmpdir := t.TempDir()
	tmpwav := filepath.Join(tmpdir, "audio.temp.wav")
	err := ioutil.WriteFile(tmpwav, []byte("abc"), 0644)
	if err != nil {
		t.Fatal(err)
	}
	called := []interface{}{}

	origCheckOutput := audiogrep.CheckOutput
	origPathExists := audiogrep.PathExists
	origRemove := audiogrep.Remove
	origOpenWriter := audiogrep.OpenWriter
	defer func() {
		audiogrep.CheckOutput = origCheckOutput
		audiogrep.PathExists = origPathExists
		audiogrep.Remove = origRemove
		audiogrep.OpenWriter = origOpenWriter
	}()

	audiogrep.CheckOutput = func(args []string) ([]byte, error) {
		called = append(called, args)
		return []byte("abc junk\n"), nil
	}

	filesCreated := map[string]bool{}
	audiogrep.PathExists = func(f string) bool {
		if strings.HasSuffix(f, ".transcription.txt") {
			return filesCreated[f]
		}
		_, err := os.Stat(f)
		return err == nil
	}
	audiogrep.Remove = func(f string) error {
		called = append(called, []interface{}{"rm", f})
		filesCreated[f] = false
		return nil
	}
	audiogrep.OpenWriter = func(name string) (func([]byte) error, func() error, error) {
		filesCreated[name] = true
		f, err := os.Create(name)
		if err != nil {
			return nil, nil, err
		}
		write := func(b []byte) error {
			_, err := f.Write(b)
			return err
		}
		close := f.Close
		return write, close, nil
	}

	outname := filepath.Join(tmpdir, "audio.transcription.txt")
	if _, err := os.Stat(outname); err == nil {
		os.Remove(outname)
	}

	err = audiogrep.Transcribe([]string{tmpwav}, 1, 1)
	if err != nil {
		t.Fatalf("Transcribe failed: %v", err)
	}

	rmSeen := false
	for _, it := range called {
		if arr, ok := it.([]interface{}); ok && len(arr) >= 2 {
			if arr[0] == "rm" {
				rmSeen = true
			}
		}
	}
	if !rmSeen {
		t.Error("Expected remove call")
	}
	if !filesCreated[outname] {
		t.Error("Expected .transcription.txt creation")
	}
}

func TestSearchModes(t *testing.T) {
	tmpdir := t.TempDir()
	fn := filepath.Join(tmpdir, "s.transcription.txt")
	lines := []string{
		"<s> 0.0 1.0 1\n", "foo 1.0 1.1 1\n", "bar 1.1 1.2 1\n", "</s> 1.2 2.0 1\n",
	}
	if err := ioutil.WriteFile(fn, []byte(strings.Join(lines, "")), 0644); err != nil {
		t.Fatal(err)
	}

	origFragmentSearch := audiogrep.FragmentSearch
	origWordSearch := audiogrep.WordSearch
	origFrankenSentence := audiogrep.FrankenSentence
	origConvertTimestamps := audiogrep.ConvertTimestamps
	defer func() {
		audiogrep.FragmentSearch = origFragmentSearch
		audiogrep.WordSearch = origWordSearch
		audiogrep.FrankenSentence = origFrankenSentence
		audiogrep.ConvertTimestamps = origConvertTimestamps
	}()

	audiogrep.FragmentSearch = func(q string, s []audiogrep.Sentence, reg bool) []map[string]interface{} {
		return []map[string]interface{}{{"foo": "bar"}}
	}
	audiogrep.WordSearch = func(q string, s []audiogrep.Sentence, reg bool) []map[string]interface{} {
		return []map[string]interface{}{{"baz": 1}}
	}
	audiogrep.FrankenSentence = func(q string, fs []audiogrep.Sentence) []interface{} {
		return []interface{}{42}
	}
	audiogrep.ConvertTimestamps = func(_ []string) ([]audiogrep.Sentence, error) {
		return []audiogrep.Sentence{
			{Words: [][]string{{"foo", "1", "2", "1"}}, File: fn},
		}, nil
	}

	out := audiogrep.Search("foo", []string{fn}, "fragment", false)
	if len(out) == 0 || out[0]["foo"] != "bar" {
		t.Errorf("fragment_search dispatch failed")
	}
	out2 := audiogrep.Search("foo", []string{fn}, "word", false)
	if len(out2) == 0 || out2[0]["baz"] != 1 {
		t.Errorf("word_search dispatch failed got %+v", out2)
	}
	out3 := audiogrep.Search("foo", []string{fn}, "franken", false)
	if !reflect.DeepEqual(out3, []interface{}{42}) {
		t.Errorf("franken_sentence dispatch failed, got %+v", out3)
	}
}

func TestSearchSentence(t *testing.T) {
	tmpdir := t.TempDir()
	fn := filepath.Join(tmpdir, "a.transcription.txt")
	lines := []string{
		"<s> 0.0 0.1 1\n", "foo 0.1 0.2 1\n", "</s> 0.2 0.3 1\n",
		"<s> 0.4 0.5 1\n", "bar 0.5 0.6 1\n", "</s> 0.6 0.7 1\n",
	}
	err := ioutil.WriteFile(fn, []byte(strings.Join(lines, "")), 0644)
	if err != nil {
		t.Fatal(err)
	}
	out := audiogrep.Search("foo", []string{fn}, "", false)
	if !reflect.TypeOf(out).Implements(reflect.TypeOf([]map[string]interface{}{})) {
		t.Errorf("Result not a []map[string]interface{}")
	}
	found := false
	for _, sent := range out {
		if words, ok := sent["words"].([][]string); ok {
			s := []string{}
			for _, w := range words {
				s = append(s, w[0])
			}
			if strings.Contains(strings.Join(s, " "), "foo") {
				found = true
				break
			}
		}
	}
	if !(found || len(out) == 0) {
		t.Errorf("Should find foo in output or output may be empty, got %+v", out)
	}
}

func TestFragmentSearchEmpty(t *testing.T) {
	sent := audiogrep.FragmentSearch("notfound",
		[]audiogrep.Sentence{{Words: [][]string{{"a", "0", "1", "1"}}, File: "testfile"}}, false)
	if len(sent) != 0 {
		t.Errorf("Expected empty result, got %v", sent)
	}
}

func TestWordSearchEmpty(t *testing.T) {
	sent := audiogrep.WordSearch("notfound",
		[]audiogrep.Sentence{{Words: [][]string{{"a", "0", "1", "1"}}, File: "testfile"}}, false)
	if len(sent) != 0 {
		t.Errorf("Expected empty result, got %v", sent)
	}
}

func TestFrankenSentenceEmpty(t *testing.T) {
	origSearch := audiogrep.Search
	defer func() { audiogrep.Search = origSearch }()
	audiogrep.Search = func(q string, fs []string, mode string, reg bool) []map[string]interface{} {
		return nil
	}
	s := audiogrep.FrankenSentence("notfound", []audiogrep.Sentence{{Words: [][]string{{"a", "0", "1", "1"}}, File: "testfile"}})
	if len(s) != 0 {
		t.Errorf("Expected empty franken_sentence, got %v", s)
	}
}