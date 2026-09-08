package original

import (
	"encoding/hex"
	"encoding/json"
	"os"
	"strings"
	"testing"

	mn "trezor_mnemonic/src/mnemonic"
)

type VectorsFile map[string][][]string

func TestGenerateEntropyLengths(t *testing.T) {
	mnemoEn := mn.NewMnemonic("english", nil)
	strengths := []int{128, 160, 192, 224, 256}
	for _, s := range strengths {
		phrase := mnemoEn.Generate(s)
		if _, ok := phrase.(string); !ok {
			t.Errorf("Expected string, got %T", phrase)
		}
		words := strings.Split(phrase, " ")
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

func TestGenerateInvalidStrength(t *testing.T) {
	mnemoEn := mn.NewMnemonic("english", nil)
	badStrengths := []int{0, 132, 300, 1000}
	for _, s := range badStrengths {
		defer func() {
			if r := recover(); r == nil {
				t.Errorf("Expected panic for invalid strength %d", s)
			}
		}()
		mnemoEn.Generate(s)
	}
}

func TestCheckValid(t *testing.T) {
	mnemoEn := mn.NewMnemonic("english", nil)
	phrase := mnemoEn.Generate(128)
	if !mnemoEn.Check(phrase).(bool) {
		t.Errorf("Valid phrase did not check")
	}
}

func TestCheckInvalid(t *testing.T) {
	mnemoEn := mn.NewMnemonic("english", nil)
	phrase := "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon wrong"
	if mnemoEn.Check(phrase).(bool) {
		t.Errorf("Invalid phrase checked true")
	}
}

func TestToMnemonicAndToEntropy(t *testing.T) {
	mnemoEn := mn.NewMnemonic("english", nil)
	entropy := "00000000000000000000000000000000"
	entbytes, _ := hex.DecodeString(entropy)
	mnemonic := mnemoEn.ToMnemonic(entbytes)
	if _, ok := mnemonic.(string); !ok {
		t.Errorf("Expected string, got %T", mnemonic)
	}
	recovered := mnemoEn.ToEntropy(mnemonic)
	recbytes := recovered.([]byte)
	if !EqualBytes(recbytes, entbytes) {
		t.Errorf("Recovered entropy mismatch")
	}
}

func TestJapaneseNoSpace(t *testing.T) {
	mnemoJp := mn.NewMnemonic("japanese", nil)
	mnemonic := mnemoJp.Generate(128)
	if !strings.Contains(mnemonic, "\u3000") {
		t.Errorf("Japanese mnemonic does not contain ideographic space")
	}
}

func TestVectors(t *testing.T) {
	vectorsFile := "vectors.json"
	mnemo := mn.NewMnemonic("english", nil)
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
		for _, v := range vecs {
			if !mnemoLang.Check(v[1]).(bool) {
				t.Errorf("Vector check failed for lang=%s", lang)
			}
			want, _ := hex.DecodeString(v[0])
			got := mnemoLang.ToEntropy(v[1]).([]byte)
			if !EqualBytes(got, want) {
				t.Errorf("Vector entropy mismatch for lang=%s", lang)
			}
		}
	}
}

func TestLanguageList(t *testing.T) {
	langs := mn.ListLanguages()
	foundEn, foundFr := false, false
	for _, l := range langs {
		if l == "english" {
			foundEn = true
		}
		if l == "french" {
			foundFr = true
		}
	}
	if !foundEn || !foundFr {
		t.Errorf("Did not find both english and french in languages")
	}
}

func TestNormalizeString(t *testing.T) {
	inStr := "E͏xample   String"
	out := mn.NormalizeString(inStr)
	if !strings.Contains(out, "xample") || !strings.Contains(out, "String") {
		t.Errorf("Normalized string missing expected parts: %s", out)
	}
}

func TestExpandWord(t *testing.T) {
	mnemoEn := mn.NewMnemonic("english", nil)
	prefix := "aban"
	expanded := mnemoEn.ExpandWord(prefix)
	if _, ok := expanded.(string); !ok {
		t.Errorf("Expected string from ExpandWord")
	}
	if !strings.HasPrefix(expanded, prefix) {
		t.Errorf("Expanded word does not have prefix")
	}
}

func TestExpand(t *testing.T) {
	mnemoEn := mn.NewMnemonic("english", nil)
	phrase := "aban abou above"
	expanded := mnemoEn.Expand(phrase)
	expStr := expanded.(string)
	if !strings.Contains(expStr, "abandon") ||
		!strings.Contains(expStr, "about") ||
		!strings.Contains(expStr, "above") {
		t.Errorf("Expanded phrase is missing expanded components: %s", expStr)
	}
}

// EqualBytes checks two slices for equality
func EqualBytes(a, b []byte) bool {
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