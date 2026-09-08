package tests

import (
	"archive/zip"
	"bytes"
	"encoding/gob"
	"errors"
	"io"
	"os"
	"path/filepath"
	"reflect"
	"testing"
)

// ---- Mock & Helper Types/Functions ----

type UntypedStorage struct {
	Value interface{}
}

type FakeTorch struct {
	Dtype string
}

func (f FakeTorch) UntypedStorageClass(v interface{}) *UntypedStorage {
	return &UntypedStorage{Value: v}
}

// Tidy function: Recursively walk data, tidy dict, list, tuple as per original
func tidy(val interface{}) interface{} {
	switch v := val.(type) {
	case map[string]interface{}:
		res := make(map[string]interface{}, len(v))
		for k, vv := range v {
			res[k] = tidy(vv)
		}
		return res
	case []interface{}:
		res := make([]interface{}, len(v))
		for i, vv := range v {
			res[i] = tidy(vv)
		}
		return res
	case [2]interface{}:
		return [2]interface{}{tidy(v[0]), tidy(v[1])}
	default:
		return val
	}
}

// FakeStorage struct to mimic Python class
type FakeStorage struct {
	dtype           string
	_untypedStorage *UntypedStorage
}

func NewFakeStorage() *FakeStorage {
	return &FakeStorage{
		dtype:           "float32",
		_untypedStorage: &UntypedStorage{Value: nil},
	}
}

// UnpicklerWrapper: In Python, this is a pickle Unpickler. In Go, mimic the interface for test only

type UnpicklerWrapper struct {
	data []byte
}

func NewUnpicklerWrapper(data []byte) *UnpicklerWrapper {
	return &UnpicklerWrapper{data: data}
}

func (uw *UnpicklerWrapper) PersistentLoad(id string) *FakeStorage {
	return NewFakeStorage()
}

// Helper for zip with data.pkl
func makeZipWithDataPkl(obj interface{}, filename string, extra bool) (string, error) {
	tempfile, err := os.CreateTemp("", "*.zip")
	if err != nil {
		return "", err
	}
	defer tempfile.Close()

	buf := new(bytes.Buffer)
	enc := gob.NewEncoder(buf)
	if err := enc.Encode(obj); err != nil {
		return "", err
	}

	zipWriter := zip.NewWriter(tempfile)
	f, err := zipWriter.Create(filename)
	if err != nil {
		return "", err
	}
	if _, err := f.Write(buf.Bytes()); err != nil {
		return "", err
	}
	if extra {
		fx, _ := zipWriter.Create("data2.pkl")
		fx.Write([]byte("data2"))
	}
	if err := zipWriter.Close(); err != nil {
		return "", err
	}
	return tempfile.Name(), nil
}

func peek(zipPath string) (map[string]interface{}, error) {
	r, err := zip.OpenReader(zipPath)
	if err != nil {
		return nil, err
	}
	defer r.Close()
	var pkls []string
	for _, f := range r.File {
		if filepath.Base(f.Name) == "data.pkl" {
			pkls = append(pkls, f.Name)
		}
	}
	if len(pkls) > 1 {
		return nil, errors.New("Found two data.pkl")
	}
	if len(pkls) == 0 {
		return nil, errors.New("No data.pkl found")
	}
	f, err := r.File[0].Open()
	if err != nil {
		return nil, err
	}
	defer f.Close()
	var result map[string]interface{}
	dec := gob.NewDecoder(f)
	err = dec.Decode(&result)
	if err != nil {
		return nil, err
	}
	return result, nil
}

// ---- Tests ----

func TestTidyDictAndListTuple(t *testing.T) {
	d := map[string]interface{}{
		"a": []interface{}{1, 2, map[string]interface{}{"b": [2]interface{}{3, nil}}},
		"c": [2]interface{}{4, 5},
	}
	want := map[string]interface{}{
		"a": []interface{}{1, 2, map[string]interface{}{"b": [2]interface{}{3, nil}}},
		"c": [2]interface{}{4, 5},
	}
	got := tidy(d)
	if !reflect.DeepEqual(got, want) {
		t.Errorf("tidy() = %v, want %v", got, want)
	}
}

func TestTidyBaseTypes(t *testing.T) {
	vals := []interface{}{nil, 3, 0.1, "foo", true}
	for _, v := range vals {
		got := tidy(v)
		if got != v {
			t.Errorf("tidy(%v) = %v, want %v", v, got, v)
		}
	}
}

func TestTidyUnknownType(t *testing.T) {
	type Foo struct{}
	f := Foo{}
	got := tidy(f)
	if got != f {
		t.Errorf("tidy(unknownType) = %v, want %v", got, f)
	}
}

func TestFakeStorageConstruction(t *testing.T) {
	s := NewFakeStorage()
	if s.dtype == "" {
		t.Errorf("dtype should be set")
	}
	if s._untypedStorage == nil {
		t.Errorf("should have _untypedStorage")
	}
}

func TestUnpicklerWrapper(t *testing.T) {
	var buf bytes.Buffer
	enc := gob.NewEncoder(&buf)
	err := enc.Encode("abc")
	if err != nil {
		t.Fatal("failed to encode test data:", err)
	}
	data := buf.Bytes()
	uw := NewUnpicklerWrapper(data)
	res := uw.PersistentLoad("id")
	if res == nil {
		t.Errorf("PersistentLoad did not return FakeStorage")
	}
}

func TestPeekSingleDataPkl(t *testing.T) {
	obj := map[string]interface{}{"foo": 1}
	zfile, err := makeZipWithDataPkl(obj, "data.pkl", false)
	if err != nil {
		t.Fatal("error creating zip:", err)
	}
	defer os.Remove(zfile)
	got, err := peek(zfile)
	if err != nil {
		t.Fatalf("peek failed: %v", err)
	}
	if v, ok := got["foo"]; !ok || v != 1.0 && v != 1 {
		t.Errorf("peek() = %v, want foo==1", got)
	}
}

func TestPeekDuplicateDataPkl(t *testing.T) {
	// Simulate two "data.pkl" files by putting in distinct folder paths
	tempfile, err := os.CreateTemp("", "*.zip")
	if err != nil {
		t.Fatal(err)
	}
	defer os.Remove(tempfile.Name())
	zipWriter := zip.NewWriter(tempfile)
	bufx := new(bytes.Buffer)
	gob.NewEncoder(bufx).Encode(map[string]interface{}{"x": 1})
	bufy := new(bytes.Buffer)
	gob.NewEncoder(bufy).Encode(map[string]interface{}{"y": 2})

	fx, _ := zipWriter.Create("first/data.pkl")
	fx.Write(bufx.Bytes())
	fy, _ := zipWriter.Create("second/data.pkl")
	fy.Write(bufy.Bytes())

	zipWriter.Close()
	tempfile.Close()
	_, errPeek := peek(tempfile.Name())
	if errPeek == nil || errPeek.Error() != "Found two data.pkl" {
		t.Errorf("expected error on duplicate data.pkl, got %v", errPeek)
	}
}