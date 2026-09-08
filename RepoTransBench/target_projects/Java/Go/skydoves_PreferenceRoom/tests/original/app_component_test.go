package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"skydoves/preferenceroom/tests"
)

type AppComponent struct{}

func (ac *AppComponent) UserProfile() interface{} {
	return struct{}{}
}
func (ac *AppComponent) UserDevice() interface{} {
	return struct{}{}
}
func (ac *AppComponent) GetEntityNameList() []string {
	return []string{"UserProfile", "UserDevice"}
}
func GetAppComponentInstance() *AppComponent {
	return &AppComponent{}
}

func TestComponentInitialize(t *testing.T) {
	assert.NotNil(t, GetAppComponentInstance())
}

func TestEntityInitialize(t *testing.T) {
	ac := GetAppComponentInstance()
	assert.NotNil(t, ac.UserProfile())
	assert.NotNil(t, ac.UserDevice())
}

func TestEntityList(t *testing.T) {
	ac := GetAppComponentInstance()
	list := ac.GetEntityNameList()
	assert.Equal(t, "UserProfile", list[0])
	assert.Equal(t, "UserDevice", list[1])
}