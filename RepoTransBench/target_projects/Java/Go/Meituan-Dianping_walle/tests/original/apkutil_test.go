package original

import (
	"errors"
	"os"
	"testing"
)

type ApkUtil struct{}

type Pair struct {
	First  interface{}
	Second interface{}
}

func (a *ApkUtil) GetApkSigningBlock(f *os.File) error {
	if f == nil {
		return errors.New("nil input")
	}
	return nil
}

func (a *ApkUtil) GetMapIdValue(arr []Pair, id int64) interface{} {
	// Return nil if array is empty
	if len(arr) == 0 {
		return nil
	}
	for _, p := range arr {
		if p.First == id {
			return p.Second
		}
	}
	return nil
}

func (a *ApkUtil) FindApkSignatureSchemeV2BlockId(f *os.File) error {
	if f == nil {
		return errors.New("nil input")
	}
	_, err := os.Stat(f.Name())
	if err != nil {
		return err
	}
	return nil
}

func TestApkUtil_GetApkSigningBlock_NullInput(t *testing.T) {
	apkUtil := &ApkUtil{}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Should panic for nil input")
		}
	}()
	apkUtil.GetApkSigningBlock(nil)
}

func TestApkUtil_GetMapIdValue_EmptyArray(t *testing.T) {
	apkUtil := &ApkUtil{}
	if apkUtil.GetMapIdValue([]Pair{}, 0) != nil {
		t.Fatalf("should return nil for empty input")
	}
}

func TestApkUtil_FindApkSignatureSchemeV2BlockId(t *testing.T) {
	apkUtil := &ApkUtil{}
	dummyFile := "non-existent.apk"
	file, err := os.Open(dummyFile)
	// file won't exist, simulate error
	if err == nil {
		file.Close()
	}
	err = apkUtil.FindApkSignatureSchemeV2BlockId(&os.File{Name: func() string { return dummyFile }()})
	if err == nil {
		t.Fatalf("Should throw error for non-existent file")
	}
}