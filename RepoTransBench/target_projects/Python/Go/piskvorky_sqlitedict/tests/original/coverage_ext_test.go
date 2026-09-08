package original

import (
	"os"
	"testing"
	// import path is project-root-relative; adjust when implementing sqlitedict.go
	. "piskvorky_sqlitedict"
)

func TestEncodeDecode(t *testing.T) {
	d := map[string]interface{}{"a": 1, "b": 2}
	b, err := Encode(d)
	if err != nil {
		t.Fatalf("Encode error: %v", err)
	}
	decoded, err := Decode(b)
	if err != nil {
		t.Fatalf("Decode error: %v", err)
	}
	got, ok := decoded.(map[string]interface{})
	if !ok {
		t.Fatalf("Decode result wrong type")
	}
	if len(got) != 2 || got["a"] != 1.0 || got["b"] != 2.0 {
		t.Errorf("Decode got %+v, want map[a:1 b:2]", got)
	}
}

func TestEncodeDecodeKey(t *testing.T) {
	k := "mykey"
	kb, err := EncodeKey(k)
	if err != nil {
		t.Fatalf("EncodeKey error: %v", err)
	}
	dec, err := DecodeKey(kb)
	if err != nil {
		t.Fatalf("DecodeKey error: %v", err)
	}
	if dec != k {
		t.Errorf("DecodeKey(%q) = %q, want %q", kb, dec, k)
	}
}

func TestIdentity(t *testing.T) {
	val := "foo"
	res := Identity(val)
	if res != val {
		t.Errorf("Identity failed: got %v, want %v", res, val)
	}
}

func TestReraise(t *testing.T) {
	defer func() {
		r := recover()
		if r == nil {
			t.Fatalf("Expected panic")
		}
		err, ok := r.(error)
		if !ok {
			t.Logf("Got non-error panic: %v", r)
		} else if err.Error() != "boo" {
			t.Errorf("reraise panic = %q, want %q", err.Error(), "boo")
		}
	}()
	func() {
		defer func() {
			if e := recover(); e != nil {
				Reraise("ValueError", e)
			}
		}()
		panic("boo")
	}()
}

func TestOpenFunction(t *testing.T) {
	name := TempFile(t, "sqdict", ".sqlite")
	d, err := Open(name)
	if err != nil {
		t.Fatalf("open: %v", err)
	}
	defer d.Close()
	if err := d.Set("x", 12); err != nil {
		t.Fatalf("set: %v", err)
	}
	val, err := d.Get("x")
	if err != nil {
		t.Fatalf("get: %v", err)
	}
	if val != 12 {
		t.Errorf("Get(x) = %v, want 12", val)
	}
}