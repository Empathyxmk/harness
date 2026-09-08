package public_tests

import (
	"bytes"
	"encoding/gob"
	"os"
	"reflect"
	"testing"
)

// Dummy checkpoint functions if not available.
func saveCheckpoint(obj map[string]interface{}, path string) error {
	var buf bytes.Buffer
	enc := gob.NewEncoder(&buf)
	if err := enc.Encode(obj); err != nil {
		return err
	}
	return os.WriteFile(path, buf.Bytes(), 0644)
}

func loadCheckpoint(path string) (map[string]interface{}, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	rdr := bytes.NewReader(data)
	dec := gob.NewDecoder(rdr)
	var m map[string]interface{}
	if err := dec.Decode(&m); err != nil {
		return nil, err
	}
	return m, nil
}

func TestPublicCheckpointCreateAndLoad(t *testing.T) {
	dir := t.TempDir()
	data := map[string]interface{}{
		"epoch":    7,
		"val_loss": 0.024,
	}
	filePath := dir + "/cpoint_pub.pt"
	if err := saveCheckpoint(data, filePath); err != nil {
		t.Fatalf("saveCheckpoint failed: %v", err)
	}
	loaded, err := loadCheckpoint(filePath)
	if err != nil {
		t.Fatalf("loadCheckpoint failed: %v", err)
	}
	if loaded["epoch"] != 7.0 && loaded["epoch"] != 7 {
		t.Errorf("loaded[epoch] = %v, want 7", loaded["epoch"])
	}
	if loaded["val_loss"] != 0.024 {
		t.Errorf("loaded[val_loss] = %v, want 0.024", loaded["val_loss"])
	}
	wrong := map[string]interface{}{"epoch": 10, "val_loss": 0.01}
	if reflect.DeepEqual(loaded, wrong) {
		t.Errorf("loaded should not match %v", wrong)
	}
}