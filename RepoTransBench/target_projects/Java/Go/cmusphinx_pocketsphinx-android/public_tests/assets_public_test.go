package public_tests

import (
	"testing"
	"errors"
)

type Assets struct{
	Dest string
}

func NewAssets(_ interface{}, dest string) *Assets {
	return &Assets{Dest: dest}
}

func (a *Assets) Sync() error {
	return errors.New("sync cannot proceed (simulated)")
}

func TestAssetsConstructorWithDifferentDest(t *testing.T) {
	assets := NewAssets(nil, "public_dest_dir_v2")
	if assets == nil {
		t.Fatal("Expected non-nil assets")
	}
}

func TestSyncMethodThrowsExceptionWithPublicData(t *testing.T) {
	assets := NewAssets(nil, "public_dest_dir_v2")
	err := assets.Sync()
	if err == nil {
		t.Fatal("Expected error in Sync")
	}
}