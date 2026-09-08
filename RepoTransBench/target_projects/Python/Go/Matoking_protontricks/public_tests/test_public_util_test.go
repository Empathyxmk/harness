package public_tests

import (
	"reflect"
	"testing"
)

func lowerDictGo(in map[string]interface{}) map[string]interface{} {
	out := make(map[string]interface{})
	for k, v := range in {
		key := k
		skey, ok := key.(string)
		if ok {
			key = lowerAscii(skey)
		}
		val := v
		if mp, ok := v.(map[string]interface{}); ok {
			val = lowerDictGo(mp)
		}
		out[key.(string)] = val
	}
	return out
}
func lowerAscii(s string) string {
	out := []rune{}
	for _, c := range s {
		if c >= 'A' && c <= 'Z' {
			c = c + 32
		}
		out = append(out, c)
	}
	return string(out)
}

func TestPublicLowerDict(t *testing.T) {
	upperDict := map[string]interface{}{
		"KEY":   10,
		"ALPHA": 20,
		"Z":     "VALUE",
		"MiXeD": "Flag",
		"foo":   "Bar",
	}
	want := map[string]interface{}{
		"key":   10,
		"alpha": 20,
		"z":     "VALUE",
		"mixed": "Flag",
		"foo":   "Bar",
	}
	got := lowerDictGo(upperDict)
	if !reflect.DeepEqual(got, want) {
		t.Errorf("lowerDictGo() = %#v, want %#v", got, want)
	}
}