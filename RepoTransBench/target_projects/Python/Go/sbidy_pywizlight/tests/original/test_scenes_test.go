package original

import (
	"testing"
)

var sceneNameToId = map[string]int{
	"Alarm": 35,
}

func GetIDFromSceneName(name string) (int, error) {
	id, ok := sceneNameToId[name]
	if !ok {
		return 0, ErrSceneNotFound{name}
	}
	return id, nil
}

type ErrSceneNotFound struct{ Name string }
func (e ErrSceneNotFound) Error() string { return "scene " + e.Name + " not found" }

func TestGetIDFromSceneName(t *testing.T) {
	_, err := GetIDFromSceneName("non_exist")
	if err == nil {
		t.Error("expected error for non_exist scene name")
	}
	id, err := GetIDFromSceneName("Alarm")
	if err != nil {
		t.Errorf("unexpected error: %v", err)
	}
	if id != 35 {
		t.Errorf("expected id 35 for Alarm, got %d", id)
	}
}