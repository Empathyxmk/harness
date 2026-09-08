package original

import (
	"testing"

	"mohak1712_uberux/tests"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

func TestMapActivityOnCreateExecutesWithoutCrash(t *testing.T) {
	a := new(tests.MapActivity)
	a.On("OnCreate", mock.Anything).Return()
	a.OnCreate(tests.Bundle{})
	assert.NotNil(t, a)
}

func TestMapActivityPageTransformerNoCrash(t *testing.T) {
	a := tests.NewMapActivity()
	assert.NotNil(t, a.PageTransformer)
}

func TestMapActivityPageChangeListenerNoCrash(t *testing.T) {
	a := tests.NewMapActivity()
	plc := a.PageChangeListener
	plc.OnPageScrollStateChanged(0)
	plc.OnPageSelected(0)
	plc.OnPageScrolled(0, 0.5, 20)
	assert.NotNil(t, plc)
}