package public_tests

import (
	"testing"
)

type MockCircleMenu struct {
	openMenuCalls  int
	closeMenuCalls int
}

func (m *MockCircleMenu) OpenMenu() {
	m.openMenuCalls++
}

func (m *MockCircleMenu) CloseMenu() {
	m.closeMenuCalls++
}

type MainActivity struct {
	CircleMenu *MockCircleMenu
}

func NewMainActivity(cm *MockCircleMenu) *MainActivity {
	return &MainActivity{CircleMenu: cm}
}

func (m *MainActivity) OnMenuOpened(_ int, _ interface{}) bool {
	m.CircleMenu.OpenMenu()
	return false
}

func (m *MainActivity) OnBackPressed() {
	m.CircleMenu.CloseMenu()
}

func TestOnMenuOpenedCallsOpenMenuTwice(t *testing.T) {
	mockCircleMenu := &MockCircleMenu{}
	mainActivity := NewMainActivity(mockCircleMenu)

	mainActivity.OnMenuOpened(2, nil)
	mainActivity.OnMenuOpened(3, nil)
	if mockCircleMenu.openMenuCalls != 2 {
		t.Errorf("Expected OpenMenu to be called twice, got %d", mockCircleMenu.openMenuCalls)
	}
}

func TestOnBackPressedCallsCloseMenuMultipleTimes(t *testing.T) {
	mockCircleMenu := &MockCircleMenu{}
	mainActivity := NewMainActivity(mockCircleMenu)

	mainActivity.OnBackPressed()
	mainActivity.OnBackPressed()
	if mockCircleMenu.closeMenuCalls != 2 {
		t.Errorf("Expected CloseMenu to be called twice, got %d", mockCircleMenu.closeMenuCalls)
	}
}