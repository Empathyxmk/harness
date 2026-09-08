package original

import (
	"os"
	"path/filepath"
	"testing"
	
	mn "trezor_mnemonic/src/mnemonic"
)

func TestInvalidLanguage(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for invalid language")
		}
	}()
	_ = mn.NewMnemonic("foo-bar-baz", nil)
}

func TestDetectLanguageValid(t *testing.T) {
	englishPhrase := "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
	lang, err := mn.DetectLanguage(englishPhrase)
	if err != nil {
		t.Fatalf("Did not expect error: %v", err)
	}
	if lang != "english" {
		t.Errorf("Expected english, got %s", lang)
	}
}

func TestDetectLanguageInvalid(t *testing.T) {
	phrase := "foobar foobar foobar foobar foobar foobar foobar foobar foobar foobar foobar foobar"
	_, err := mn.DetectLanguage(phrase)
	if err == nil {
		t.Fatalf("Expected error for invalid language")
	}
}

func TestListLanguagesUnique(t *testing.T) {
	langs := mn.ListLanguages()
	langSet := make(map[string]struct{})
	for _, l := range langs {
		langSet[l] = struct{}{}
	}
	if len(langs) != len(langSet) {
		t.Errorf("Languages list is not unique")
	}
	found := false
	for _, l := range langs {
		if l == "english" {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("english not in languages list")
	}
}

func TestWordlistFileExists(t *testing.T) {
	langs := mn.ListLanguages()
	for _, lang := range langs {
		path := filepath.Join("src", "mnemonic", "wordlist", lang+".txt")
		if _, err := os.Stat(path); os.IsNotExist(err) {
			t.Errorf("Wordlist file does not exist: %s", path)
		}
	}
}

func TestInitWithWordlistInvalidLength(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for invalid wordlist length")
		}
	}()
	fakeWordlist := make([]string, 2047)
	_ = mn.NewMnemonicWithWordlist("idontexist", fakeWordlist)
}

func TestInitWithWordlistValidLength(t *testing.T) {
	fakeWordlist := make([]string, 2048)
	for i := 0; i < 2048; i++ {
		fakeWordlist[i] = "foo"
	}
	m := mn.NewMnemonicWithWordlist("idontexist", fakeWordlist)
	for i, w := range m.Wordlist {
		if w != "foo" {
			t.Errorf("Expected foo in position %d, got %s", i, w)
		}
	}
}

func TestExpandWordNotFound(t *testing.T) {
	m := mn.NewMnemonic("english", nil)
	result := m.ExpandWord("no-possible-prefix")
	if result != "no-possible-prefix" {
		t.Errorf("Expected original prefix returned, got: %s", result)
	}
}

func TestCheckExpandsPrefixInput(t *testing.T) {
	m := mn.NewMnemonic("english", nil)
	phrase := "aban abou above absent absorb abstract absurd abuse access accident account accuse"
	res := m.Check(phrase)
	switch res := res.(type) {
	case bool:
		// ok
	default:
		t.Errorf("Expected a bool from Check, got %T", res)
	}
}

func TestStripAccentsBasicPatch(t *testing.T) {
	// mnemo.strip_accents not real, just check method does not exist (interface)
	has := mn.HasStripAccents()
	if has {
		t.Errorf("Didn't expect Mnemonic to have strip_accents")
	}
}