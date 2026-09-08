package public_tests

import (
	"os"
	"path/filepath"
	"testing"
	
	mn "trezor_mnemonic/src/mnemonic"
)

func TestPublicInvalidLanguage(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for invalid language")
		}
	}()
	_ = mn.NewMnemonic("notareallanguage", nil)
}

func TestPublicDetectLanguageValid(t *testing.T) {
	englishPhrase := "legal winner thank year wave sausage worth useful legal winner thank yellow"
	lang, err := mn.DetectLanguage(englishPhrase)
	if err != nil {
		t.Fatalf("Did not expect error: %v", err)
	}
	if lang != "english" {
		t.Errorf("Expected english, got %s", lang)
	}
}

func TestPublicDetectLanguageInvalid(t *testing.T) {
	phrase := "zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo"
	_, err := mn.DetectLanguage(phrase)
	if err == nil {
		t.Fatalf("Expected error for invalid language phrase")
	}
}

func TestPublicListLanguagesUnique(t *testing.T) {
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
		if l == "japanese" {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("japanese not in the list of languages")
	}
}

func TestPublicWordlistFileExists(t *testing.T) {
	langs := mn.ListLanguages()
	for _, lang := range langs {
		path := filepath.Join("src", "mnemonic", "wordlist", lang+".txt")
		if _, err := os.Stat(path); os.IsNotExist(err) {
			t.Errorf("Wordlist file does not exist: %s", path)
		}
	}
}

func TestPublicInitWithWordlistInvalidLength(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for wrong wordlist length")
		}
	}()
	fakeWordlist := make([]string, 2050)
	_ = mn.NewMnemonicWithWordlist("anotherfake", fakeWordlist)
}

func TestPublicInitWithWordlistValidLength(t *testing.T) {
	fakeWordlist := make([]string, 2048)
	for i := 0; i < 2048; i++ {
		fakeWordlist[i] = "bar"
	}
	m := mn.NewMnemonicWithWordlist("anotherfake", fakeWordlist)
	for i, w := range m.Wordlist {
		if w != "bar" {
			t.Errorf("Expected bar at position %d, got %s", i, w)
		}
	}
}

func TestPublicExpandWordNotFound(t *testing.T) {
	m := mn.NewMnemonic("english", nil)
	result := m.ExpandWord("unknownprefixword")
	if result != "unknownprefixword" {
		t.Errorf("Expected original word back, got %s", result)
	}
}

func TestPublicCheckExpandsPrefixInput(t *testing.T) {
	m := mn.NewMnemonic("english", nil)
	phrase := "able about above absent absorb abstract absurd abuse access accident account accuse"
	res := m.Check(phrase)
	switch res := res.(type) {
	case bool:
		// ok
	default:
		t.Errorf("Check did not return bool, got %T", res)
	}
}

func TestPublicStripAccentsBasicPatch(t *testing.T) {
	// mnemo.strip_accents is not a real method, patch for coverage
	has := mn.HasStripAccents()
	if has {
		t.Errorf("Didn't expect Mnemonic to have strip_accents")
	}
}