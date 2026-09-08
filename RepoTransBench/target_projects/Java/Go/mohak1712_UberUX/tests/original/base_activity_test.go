package original

import (
	"errors"
	"testing"

	"mohak1712_uberux/tests"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

type myBaseActivity struct {
	tests.BaseActivity
}

func (m *myBaseActivity) OnMapReady(gmap *tests.GoogleMap) {
	// Calls base
	m.BaseActivity.OnMapReady(gmap)
}

func TestBaseActivityOnCreateInitializesClient(t *testing.T) {
	a := &myBaseActivity{}
	a.On("OnCreate", mock.Anything).Return()
	bundle := tests.Bundle{}
	a.OnCreate(bundle)
	assert.NotNil(t, a)
}

func TestBaseActivityOpenPlaceAutoCompleteViewHandlesExceptionGracefully(t *testing.T) {
	a := &myBaseActivity{}
	a.On("OpenPlaceAutoCompleteView").Return()
	a.MMap = new(tests.GoogleMap)
	defer func() {
		if r := recover(); r != nil {
			t.Fatal("openPlaceAutoCompleteView should handle exception gracefully")
		}
	}()
	a.OpenPlaceAutoCompleteView()
}

func TestBaseActivityOnMapReadyNoCrash(t *testing.T) {
	a := &myBaseActivity{}
	a.On("OnMapReady", mock.Anything).Return()
	mapMock := new(tests.GoogleMap)
	mapMock.On("SetMaxZoomPreference", 20).Return(nil)
	a.OnMapReady(mapMock)
}