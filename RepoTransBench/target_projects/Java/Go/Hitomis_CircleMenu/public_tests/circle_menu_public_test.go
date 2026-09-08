package public_tests

import (
	"testing"
)

// We will fake CircleMenu type sufficient for the tests.

type SubMenu struct {
	Color     int
	IconResId int
}

type CircleMenu struct {
	mainMenuColor int
	subMenus      []SubMenu
}

// Fictitious constructor: context, attributeSet ignored
func NewCircleMenu(_, _ interface{}) *CircleMenu {
	return &CircleMenu{subMenus: []SubMenu{}}
}

func (cm *CircleMenu) SetMainMenu(color int, iconNormal int, iconPressed int) {
	cm.mainMenuColor = color
}

func (cm *CircleMenu) GetMainMenuColor() int {
	return cm.mainMenuColor
}

func (cm *CircleMenu) AddSubMenu(color int, iconResId int) {
	cm.subMenus = append(cm.subMenus, SubMenu{Color: color, IconResId: iconResId})
}

func (cm *CircleMenu) GetSubMenus() []SubMenu {
	return cm.subMenus
}

func TestSetMainMenuDifferentColor(t *testing.T) {
	circleMenu := NewCircleMenu(nil, nil)
	circleMenu.SetMainMenu(0xFF00FF00, 200, 201)
	if circleMenu.GetMainMenuColor() != 0xFF00FF00 {
		t.Errorf("Expected mainMenuColor to be 0xFF00FF00, got %#x", circleMenu.GetMainMenuColor())
	}
}

func TestAddSubMenuDifferentIcons(t *testing.T) {
	circleMenu := NewCircleMenu(nil, nil)
	circleMenu.AddSubMenu(0xFFFF0000, 300)
	subMenus := circleMenu.GetSubMenus()
	if len(subMenus) != 1 {
		t.Errorf("Expected 1 submenu, got %d", len(subMenus))
	}
	if subMenus[0].Color != 0xFFFF0000 {
		t.Errorf("Expected Color to be 0xFFFF0000, got %#x", subMenus[0].Color)
	}
	if subMenus[0].IconResId != 300 {
		t.Errorf("Expected IconResId to be 300, got %d", subMenus[0].IconResId)
	}
}