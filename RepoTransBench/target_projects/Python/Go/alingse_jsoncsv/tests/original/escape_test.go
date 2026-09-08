package original

import (
	"testing"

	"alingse_jsoncsv/jsoncsv"
)

func TestEncodeDecode_AllSep(t *testing.T) {
	path := []string{"A", "B", "..", "\\.\\ww"}
	seps := []string{"A", "B", ".", "w"}
	for _, sep := range seps {
		key := jsoncsv.EncodeSafeKey(path, sep)
		_path := jsoncsv.DecodeSafeKey(key, sep)
		for i, p := range path {
			if _path[i] != p {
				t.Errorf("at index %d: want %s, got %s", i, p, _path[i])
			}
		}
	}
}

func TestEncode(t *testing.T) {
	path := []string{"A", "B", "C", "www.xxx.com"}
	sep := "."
	key := jsoncsv.EncodeSafeKey(path, sep)
	want := "A\\.B\\.C\\.www.xxx.com"
	if key != want {
		t.Errorf("expected %s, got %s", want, key)
	}
}

func TestDecode(t *testing.T) {
	key := "A\\.B\\.C\\.www.xxx.com"
	sep := "."
	path := jsoncsv.DecodeSafeKey(key, sep)
	want := []string{"A", "B", "C", "www.xxx.com"}
	for i, w := range want {
		if path[i] != w {
			t.Errorf("at %d: want %s, got %s", i, w, path[i])
		}
	}
}