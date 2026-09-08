package public_tests

import "testing"

type DummyPresenter struct {
	Value int
}

// Uses Minutes for demonstration, but this is a logical stub for threading/timeout simulation.

func TestPresenterManagerPublicTest_SaveAndRestorePresenterWithDifferentInstance(t *testing.T) {
	pm := NewPresenterManager()
	key := "presenter1"
	presenter := &DummyPresenter{Value: 99}

	pm.SavePresenter(key, presenter)
	restored := pm.RestorePresenter(key)
	if restored == nil {
		t.Fatalf("restored presenter is nil")
	}
	rp, ok := restored.(*DummyPresenter)
	if !ok || rp.Value != 99 {
		t.Errorf("restored presenter Value mismatch: got %v, want 99", rp)
	}
}

func TestPresenterManagerPublicTest_RestorePresenterReturnsNullAfterRestoreWithDifferentTimings(t *testing.T) {
	pm := NewPresenterManager()
	key := "presenterX"
	presenter := &DummyPresenter{Value: 666}
	pm.SavePresenter(key, presenter)
	first := pm.RestorePresenter(key)
	if first == nil {
		t.Fatalf("presenter not restored on first get")
	}
	second := pm.RestorePresenter(key)
	if second != nil {
		t.Errorf("expected nil on second restore")
	}
}

func TestPresenterManagerPublicTest_GetInstanceReturnsSameSingletonInstance(t *testing.T) {
	pm1 := GetPresenterManager()
	pm2 := GetPresenterManager()
	if pm1 != pm2 {
		t.Errorf("PresenterManager should return singleton")
	}
}