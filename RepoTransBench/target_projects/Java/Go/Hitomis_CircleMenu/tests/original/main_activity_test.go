package original

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

func TestOnMenuOpenedCallsCircleMenuOpenMenu(t *testing.T) {
	mockCircleMenu := &MockCircleMenu{}
	mainActivity := NewMainActivity(mockCircleMenu)

	mainActivity.OnMenuOpened(1, nil)
	if mockCircleMenu.openMenuCalls != 1 {
		t.Errorf("Expected OpenMenu to be called once, got %d", mockCircleMenu.openMenuCalls)
	}
}

func TestOnBackPressedCallsCircleMenuCloseMenu(t *testing.T) {
	mockCircleMenu := &MockCircleMenu{}
	mainActivity := NewMainActivity(mockCircleMenu)

	mainActivity.OnBackPressed()
	if mockCircleMenu.closeMenuCalls != 1 {
		t.Errorf("Expected CloseMenu to be called once, got %d", mockCircleMenu.closeMenuCalls)
	}
}