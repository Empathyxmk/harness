package public_tests

import (
	"testing"

	"alingse_jsoncsv/jsoncsv"
)

func TestPublicAll_EncodeDecode(t *testing.T) {
	path := []string{"A1", "B1", "..2", "\\.\\oo"}
	for _, sep := range []string{"R", "E", "P"} {
		key := jsoncsv.EncodeSafeKey(path, sep)
		_path := jsoncsv.DecodeSafeKey(key, sep)
		for i, v := range path {
			if _path[i] != v {
				t.Errorf("index %d: want %s, got %s", i, v, _path[i])
			}
		}
	}
}

func TestPublicEncode(t *testing.T) {
	path := []string{"D", "E", "F", "my.site.com"}
	sep := "."
	key := jsoncsv.EncodeSafeKey(path, sep)
	want := "D\\.E\\.F\\.my.site.com"
	if key != want {
		t.Errorf("expected %q, got %q", want, key)
	}
}

func TestPublicDecode(t *testing.T) {
	key := "X\\.Y\\.Z\\.abc.def.com"
	sep := "."
	path := jsoncsv.DecodeSafeKey(key, sep)
	want := []string{"X", "Y", "Z", "abc.def.com"}
	for i, v := range want {
		if path[i] != v {
			t.Errorf("at index %d: want %s, got %s", i, v, path[i])
		}
	}
}