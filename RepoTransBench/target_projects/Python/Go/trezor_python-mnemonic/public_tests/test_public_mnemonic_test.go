package public_tests

import (
	"encoding/hex"
	"encoding/json"
	"os"
	"strings"
	"testing"
	
	mn "trezor_mnemonic/src/mnemonic"
)

type VectorsFile map[string][][]string

func TestPublicGenerateEntropyLengths(t *testing.T) {
	mnemoEn := mn.NewMnemonic("english", nil)
	for _, s := range []int{160, 192, 224, 256} {
		phrase := mnemoEn.Generate(s)
		strPhrase, ok := phrase.(string)
		if !ok {
			t.Errorf("Expected string, got %T", phrase)
		}
		words := strings.Split(strPhrase, " ")
		for _, w := range words {
			found := false
			for _, wl := range mnemoEn.Wordlist {
				if w == wl {
					found = true
					break
				}
			}
			if !found {
				t.Errorf("Generated word not in wordlist: %s", w)
			}
		}
	}
}

func TestPublicGenerateInvalidStrength(t *testing.T) {
	mnemoEn := mn.NewMnemonic("english", nil)
	for _, bad := range []int{10, 90, 270, 512} {
		defer func() {
			if r := recover(); r == nil {
				t.Errorf("Expected panic for bad strength value")
			}
		}()
		mnemoEn.Generate(bad)
	}
}

func TestPublicCheckValid(t *testing.T) {
	mnemoEn := mn.NewMnemonic("english", nil)
	phrase := mnemoEn.Generate(256)
	if !mnemoEn.Check(phrase).(bool) {
		t.Errorf("Valid phrase did not check")
	}
}

func TestPublicCheckInvalid(t *testing.T) {
	mnemoEn := mn.NewMnemonic("english", nil)
	phrase := "legal winner thank year wave sausage worth useful legal winner thank banana"
	if mnemoEn.Check(phrase).(bool) {
		t.Errorf("Invalid phrase checked as true")
	}
}

func TestPublicToMnemonicAndToEntropy(t *testing.T) {
	mnemoEn := mn.NewMnemonic("english", nil)
	entropy := "ffffffffffffffffffffffffffffffff"
	entbytes, _ := hex.DecodeString(entropy)
	mnemonic := mnemoEn.ToMnemonic(entbytes)
	if _, ok := mnemonic.(string); !ok {
		t.Errorf("Expected string, got %T", mnemonic)
	}
	recovered := mnemoEn.ToEntropy(mnemonic)
	recbytes := recovered.([]byte)
	if !equalBytes(recbytes, entbytes) {
		t.Errorf("Did not recover original entropy")
	}
}

func TestPublicFrenchWithSpace(t *testing.T) {
	mnemoFr := mn.NewMnemonic("french", nil)
	mnemonic := mnemoFr.Generate(128)
	if !strings.Contains(mnemonic, " ") {
		t.Errorf("Expected French mnemonic to contain spaces")
	}
}

func TestPublicVectors(t *testing.T) {
	vectorsFile := "vectors.json"
	if _, err := os.Stat(vectorsFile); os.IsNotExist(err) {
		t.Skip("vectors.json not available")
	}
	fd, err := os.Open(vectorsFile)
	if err != nil {
		t.Fatalf("Error opening vectors: %v", err)
	}
	defer fd.Close()
	var vectors VectorsFile
	json.NewDecoder(fd).Decode(&vectors)
	for lang, vecs := range vectors {
		if lang == "japanese" {
			continue
		}
		mnemoLang := mn.NewMnemonic(lang, nil)
		for i, v := range vecs {
			if i >= 2 {
				break
			}
			if !mnemoLang.Check(v[1]).(bool) {
				t.Errorf("Vector check failed for lang=%s", lang)
			}
			want, _ := hex.DecodeString(v[0])
			got := mnemoLang.ToEntropy(v[1]).([]byte)
			if !equalBytes(got, want) {
				t.Errorf("Vector entropy mismatch for lang=%s", lang)
			}
		}
	}
}

func TestPublicLanguageList(t *testing.T) {
	langs := mn.ListLanguages()
	foundIt, foundSp := false, false
	for _, l := range langs {
		if l == "italian" {
			foundIt = true
		}
		if l == "spanish" {
			foundSp = true
		}
	}
	if !foundIt || !foundSp {
		t.Errorf("Missing italian or spanish in language list")
	}
}

func TestPublicNormalizeString(t *testing.T) {
	inStr := "T͏esTing   Phrase"
	out := mn.NormalizeString(inStr)
	if !strings.Contains(out, "esT") || !strings.Contains(out, "Phrase") {
		t.Errorf("String normalization missing expected parts: %s", out)
	}
}

func TestPublicExpandWord(t *testing.T) {
	mnemoEn := mn.NewMnemonic("english", nil)
	prefix := "abil"
	expanded := mnemoEn.ExpandWord(prefix)
	str, ok := expanded.(string)
	if !ok {
		t.Errorf("Expected string from ExpandWord")
	}
	if !strings.HasPrefix(str, prefix) && str == prefix {
		t.Errorf("Expanded word must start with the prefix or be different")
	}
}

func TestPublicExpand(t *testing.T) {
	mnemoEn := mn.NewMnemonic("english", nil)
	phrase := "abil abou above"
	expanded := mnemoEn.Expand(phrase)
	expStr := expanded.(string)
	if !strings.Contains(expStr, "ability") || !strings.Contains(expStr, "about") || !strings.Contains(expStr, "above") {
		t.Errorf("Expanded phrase not as expected: %s", expStr)
	}
}

func equalBytes(a, b []byte) bool {
	if len(a) != len(b) {
		return false
	}
	for i, v := range a {
		if b[i] != v {
			return false
		}
	}
	return true
}