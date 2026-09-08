package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"tasomaniac_delayedprogress/delayedprogress"
)

func TestMakeMethodsPublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	assert.NotNil(t, delayedprogress.MakeDialog(looper, "pub_title", "pub_message"))
	assert.NotNil(t, delayedprogress.MakeDialog(looper, "pub_title", "pub_message", false))
	assert.NotNil(t, delayedprogress.MakeDialog(looper, "pub_title", "pub_message", false, false))
	assert.NotNil(t, delayedprogress.MakeDialog(looper, "pub_title", "pub_message", false, false, nil))
	assert.NotNil(t, delayedprogress.NewDelayedProgressDialog(looper))
}

func TestShowDelayedMethodsPublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	delayedprogress.ShowDelayed(looper, "pub_title", "pub_message").Dismiss()
	delayedprogress.ShowDelayed(looper, "pub_title", "pub_message", false).Dismiss()
	delayedprogress.ShowDelayed(looper, "pub_title", "pub_message", false, false).Dismiss()
	delayedprogress.ShowDelayed(looper, "pub_title", "pub_message", false, false, nil).Dismiss()
}

func TestDismissBeforeMinDelayShouldNotShowPublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	dialog := delayedprogress.NewDelayedProgressDialog(looper)
	dialog.SetMinDelay(1200)
	dialog.SetMinShowTime(600)
	dialog.Show()
	assert.False(t, dialog.IsShowing())
	looper.IdleFor(250)
	assert.False(t, dialog.IsShowing())
	dialog.Dismiss()
	looper.IdleFor(1200)
	assert.False(t, dialog.IsShowing())
}

func TestDismissAfterMinDelayButBeforeMinShowTimePublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	dialog := delayedprogress.NewDelayedProgressDialog(looper)
	dialog.SetMinDelay(700)
	dialog.SetMinShowTime(1500)
	dialog.Show()
	assert.False(t, dialog.IsShowing())
	looper.IdleFor(700)
	assert.True(t, dialog.IsShowing())
	looper.IdleFor(350)
	dialog.Dismiss()
	assert.True(t, dialog.IsShowing())
	looper.IdleFor(1149)
	assert.True(t, dialog.IsShowing())
	looper.IdleFor(1)
	assert.False(t, dialog.IsShowing())
}

func TestDismissAfterMinShowTimeShouldDismissImmediatelyPublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	dialog := delayedprogress.NewDelayedProgressDialog(looper)
	dialog.SetMinDelay(800)
	dialog.SetMinShowTime(1200)
	dialog.Show()
	assert.False(t, dialog.IsShowing())
	looper.IdleFor(800)
	assert.True(t, dialog.IsShowing())
	looper.IdleFor(1200)
	assert.True(t, dialog.IsShowing())
	dialog.Dismiss()
	assert.False(t, dialog.IsShowing())
}

func TestShowWithZeroMinDelayShowsImmediatelyPublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	dialog := delayedprogress.NewDelayedProgressDialog(looper)
	dialog.SetMinDelay(0)
	dialog.SetMinShowTime(900)
	dialog.Show()
	assert.True(t, dialog.IsShowing())
	dialog.Dismiss()
	looper.IdleFor(900)
	assert.False(t, dialog.IsShowing())
}

func TestDismissWhenNeverShownNoOpPublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	dialog := delayedprogress.NewDelayedProgressDialog(looper)
	dialog.SetMinDelay(1500)
	dialog.Show()
	assert.False(t, dialog.IsShowing())
	dialog.Dismiss()
	looper.IdleFor(1500)
	assert.False(t, dialog.IsShowing())
}