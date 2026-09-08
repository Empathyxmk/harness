package original

import (
	"testing"
)

type DummyPresenter struct {
	Value int
}

func TestPresenterManager_SaveAndRestorePresenter(t *testing.T) {
	pm := NewPresenterManager()
	key := "presenterKey"

	presenter := &DummyPresenter{Value: 5}
	pm.SavePresenter(key, presenter)

	restored := pm.RestorePresenter(key)
	if restored == nil {
		t.Fatal("Restored presenter is nil")
	}
	restoredPresenter, ok := restored.(*DummyPresenter)
	if !ok {
		t.Fatalf("Restored presenter is wrong type")
	}
	if restoredPresenter.Value != presenter.Value {
		t.Errorf("Presenter value does not match: got %d, want %d", restoredPresenter.Value, presenter.Value)
	}
}

func TestPresenterManager_RestorePresenterReturnsNilOnSecondRestore(t *testing.T) {
	pm := NewPresenterManager()
	key := "presenterKey"
	presenter := &DummyPresenter{Value: 8}
	pm.SavePresenter(key, presenter)

	// First restore is valid
	rest1 := pm.RestorePresenter(key)
	if rest1 == nil {
		t.Fatalf("First restore should not be nil")
	}
	// Second restore is invalid (presenter is removed on first restore)
	rest2 := pm.RestorePresenter(key)
	if rest2 != nil {
		t.Errorf("Second restore was not nil")
	}
}

func TestPresenterManager_GetInstanceReturnsSingleton(t *testing.T) {
	pm1 := GetPresenterManager()
	pm2 := GetPresenterManager()
	if pm1 != pm2 {
		t.Errorf("PresenterManager getInstance did not return the singleton")
	}
}