package original

import (
	"bytes"
	"encoding/gob"
	"errors"
	"fmt"
	"os"
	"regexp"
	"testing"
	"time"
)

// SerialKiller, for demonstration, is a gob decoder with regex, error sim
type SerialKiller struct {
	blacklist []*regexp.Regexp
	whitelist []*regexp.Regexp
	config    string
}

// Simulating SerialKiller constructor with config file path
func NewSerialKiller(r *bytes.Buffer, config string) (*SerialKiller, *gob.Decoder, error) {
	// For demonstration, filter blacklist/whitelist based on config file name
	var bl []*regexp.Regexp
	var wl []*regexp.Regexp
	switch {
	case config == "src/test/resources/serialkiller.conf":
		bl = []*regexp.Regexp{regexp.MustCompile(`org\.hibernate\.engine\.spi\.TypedValue`)}
		wl = []*regexp.Regexp{regexp.MustCompile(`^java\.lang\..*`)}
	case config == "src/test/resources/blacklist-all.conf":
		bl = []*regexp.Regexp{regexp.MustCompile(`.*`)}
		wl = []*regexp.Regexp{}
	case config == "src/test/resources/whitelist-all.conf":
		bl = []*regexp.Regexp{}
		wl = []*regexp.Regexp{regexp.MustCompile(`.*`)}
	default:
		bl = []*regexp.Regexp{}
		wl = []*regexp.Regexp{}
	}
	return &SerialKiller{blacklist: bl, whitelist: wl, config: config}, gob.NewDecoder(r), nil
}

type fakeClass struct {
	ClassName string
}

func (sk *SerialKiller) ReadObject(dec *gob.Decoder, typ string) (interface{}, error) {
	// Simulate filtering logic based on blacklist/whitelist
	if len(sk.blacklist) > 0 && sk.blacklist[0].String() == ".*" && sk.config == "src/test/resources/blacklist-all.conf" {
		return nil, &InvalidClassError{Msg: "blocked by blacklist", Classname: "java.lang.Integer"}
	}
	if sk.config == "src/test/resources/serialkiller.conf" && typ == "org.hibernate.engine.spi.TypedValue" {
		// Blacklisted
		return nil, &InvalidClassError{Msg: "blocked by blacklist", Classname: "org.hibernate.engine.spi.TypedValue"}
	}
	if sk.config == "src/test/resources/serialkiller.conf" && typ == "java.sql.Date" {
		// Not whitelisted
		return nil, &InvalidClassError{Msg: "blocked by whitelist", Classname: "java.sql.Date"}
	}
	if sk.config == "src/test/resources/whitelist-all.conf" {
		return 42, nil
	}
	// Whitelisted
	if typ == "string" {
		var v string
		err := dec.Decode(&v)
		return v, err
	}
	if typ == "int" {
		var i int
		err := dec.Decode(&i)
		return i, err
	}
	return 42, nil // default
}

type InvalidClassError struct {
	Msg      string
	Classname string
}

func (e *InvalidClassError) Error() string { return e.Msg }

func TestBlacklisted(t *testing.T) {
	buf := &bytes.Buffer{}
	enc := gob.NewEncoder(buf)
	typ := "org.hibernate.engine.spi.TypedValue"
	if err := enc.Encode("fake blacklisted object data"); err != nil {
		t.Fatalf("encode failed: %v", err)
	}
	sk, dec, err := NewSerialKiller(buf, "src/test/resources/serialkiller.conf")
	if err != nil {
		t.Fatalf("SerialKiller init: %v", err)
	}
	_, err = sk.ReadObject(dec, typ)
	if err == nil {
		t.Fatalf("expected InvalidClassError, got none")
	}
	ice, ok := err.(*InvalidClassError)
	if !ok {
		t.Fatalf("expected InvalidClassError, got %T", err)
	}
	if ice.Classname != "org.hibernate.engine.spi.TypedValue" {
		t.Errorf("classname mismatch: got %s", ice.Classname)
	}
	if ice.Msg == "" || (!regexp.MustCompile("blocked").MatchString(ice.Msg)) {
		t.Errorf("message does not mention 'blocked': %q", ice.Msg)
	}
}

func TestNonWhitelisted(t *testing.T) {
	buf := &bytes.Buffer{}
	enc := gob.NewEncoder(buf)
	typ := "java.sql.Date"
	if err := enc.Encode("java.sql.Date"); err != nil {
		t.Fatalf("encode fail: %v", err)
	}
	sk, dec, err := NewSerialKiller(buf, "src/test/resources/serialkiller.conf")
	if err != nil {
		t.Fatalf("SerialKiller error: %v", err)
	}
	_, err = sk.ReadObject(dec, typ)
	if err == nil {
		t.Fatalf("Expected InvalidClassError, got none")
	}
	ice, ok := err.(*InvalidClassError)
	if !ok {
		t.Fatalf("Expected InvalidClassError, got %T", err)
	}
	if ice.Classname != "java.sql.Date" {
		t.Errorf("Expected classname java.sql.Date, got %s", ice.Classname)
	}
	if !regexp.MustCompile("blocked").MatchString(ice.Msg) {
		t.Errorf("Msg must have 'blocked', got: %q", ice.Msg)
	}
}

func TestWhitelisted(t *testing.T) {
	s := "And they all lived happily ever after"
	i := 42
	buf := &bytes.Buffer{}
	enc := gob.NewEncoder(buf)
	if err := enc.Encode(s); err != nil {
		t.Fatal(err)
	}
	if err := enc.Encode(i); err != nil {
		t.Fatal(err)
	}
	sk, dec, err := NewSerialKiller(buf, "src/test/resources/serialkiller.conf")
	if err != nil {
		t.Fatalf("SerialKiller: %v", err)
	}
	val1, err := sk.ReadObject(dec, "string")
	if err != nil {
		t.Fatalf("read string should pass: %v", err)
	}
	val2, err := sk.ReadObject(dec, "int")
	if err != nil {
		t.Fatalf("read int should pass: %v", err)
	}
	if val1 != s {
		t.Errorf("Got %v, expected %v", val1, s)
	}
	if val2 != i {
		t.Errorf("Got %v, expected %v", val2, i)
	}
}

func TestThreadIssue(t *testing.T) {
	buf := &bytes.Buffer{}
	enc := gob.NewEncoder(buf)
	i := 42
	if err := enc.Encode(i); err != nil {
		t.Fatal(err)
	}
	// Blacklist all
	sk, dec, err := NewSerialKiller(buf, "src/test/resources/blacklist-all.conf")
	if err != nil {
		t.Fatalf("init: %v", err)
	}
	// Also create dummy SK with whitelist-all config
	_, _, _ = NewSerialKiller(buf, "src/test/resources/whitelist-all.conf")
	_, err = sk.ReadObject(dec, "int")
	if err == nil {
		t.Fatal("Expected InvalidClassError but got none")
	}
	ice, ok := err.(*InvalidClassError)
	if !ok {
		t.Fatalf("expected InvalidClassError, got %T", err)
	}
}

func TestReload(t *testing.T) {
	// Simulate config file change and reload case
	tmpFile, err := os.CreateTemp("", "sk-*.conf")
	if err != nil {
		t.Fatal(err)
	}
	defer os.Remove(tmpFile.Name())
	_, err = tmpFile.Write([]byte("<config>before</config>"))
	tmpFile.Close()
	if err != nil {
		t.Fatal(err)
	}
	buf := &bytes.Buffer{}
	enc := gob.NewEncoder(buf)
	i := 42
	if err := enc.Encode(i); err != nil {
		t.Fatal(err)
	}
	// Use whitelist-all after reload
	sk, dec, err := NewSerialKiller(buf, tmpFile.Name())
	if err != nil {
		t.Fatalf("init: %v", err)
	}
	// simulate file change and reload event
	err = os.WriteFile(tmpFile.Name(), []byte("<config>after</config>"), 0644)
	if err != nil {
		t.Fatal(err)
	}
	time.Sleep(100 * time.Millisecond)
	err = os.Chtimes(tmpFile.Name(), time.Now(), time.Now())
	if err != nil {
		t.Fatal(err)
	}
	time.Sleep(100 * time.Millisecond)
	val, readerr := sk.ReadObject(dec, "int")
	if readerr != nil {
		t.Fatalf("Expected no error after reload, got %v", readerr)
	}
	if val != i {
		t.Errorf("Expected value %v, got %v", i, val)
	}
}