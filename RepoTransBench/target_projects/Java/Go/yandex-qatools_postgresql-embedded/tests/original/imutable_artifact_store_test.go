package original

import "testing"

type testIDownloadConfig2 struct {}

type TestMutableArtifactStore struct {
	configSet bool
}
func (t *TestMutableArtifactStore) SetDownloadConfig(cfg *testIDownloadConfig2) { t.configSet = true }
func (t *TestMutableArtifactStore) RemoveFileSet(d, fs interface{})              {}
func (t *TestMutableArtifactStore) CheckDistribution(d interface{}) bool         { return false }
func (t *TestMutableArtifactStore) ExtractFileSet(d interface{}) interface{}     { return nil }

func TestSetDownloadConfig(t *testing.T) {
	store := &TestMutableArtifactStore{}
	if store.configSet {
		t.Errorf("configSet should be false initially")
	}
	store.SetDownloadConfig(nil)
	if !store.configSet {
		t.Errorf("configSet should be true after SetDownloadConfig()")
	}
}