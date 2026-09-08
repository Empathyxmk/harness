package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"tasomaniac_delayedprogress/delayedprogress"
)

func TestMakeMethods(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	assert.NotNil(t, delayedprogress.MakeDialog(looper, "title", "message"))
	assert.NotNil(t, delayedprogress.MakeDialog(looper, "title", "message", true))
	assert.NotNil(t, delayedprogress.MakeDialog(looper, "title", "message", true, true))
	assert.NotNil(t, delayedprogress.MakeDialog(looper, "title", "message", true, true, nil))
	assert.NotNil(t, delayedprogress.NewDelayedProgressDialog(looper))
}

func TestShowDelayedMethods(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	delayedprogress.ShowDelayed(looper, "title", "message").Dismiss()
	delayedprogress.ShowDelayed(looper, "title", "message", true).Dismiss()
	delayedprogress.ShowDelayed(looper, "title", "message", true, true).Dismiss()
	delayedprogress.ShowDelayed(looper, "title", "message", true, true, nil).Dismiss()
}

func TestDismissBeforeMinDelayShouldNotShow(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	dialog := delayedprogress.NewDelayedProgressDialog(looper)
	dialog.SetMinDelay(1000)
	dialog.SetMinShowTime(500)
	dialog.Show()
	assert.False(t, dialog.IsShowing())
	looper.IdleFor(200)
	assert.False(t, dialog.IsShowing())
	dialog.Dismiss()
	looper.IdleFor(1000)
	assert.False(t, dialog.IsShowing())
}

func TestDismissAfterMinDelayButBeforeMinShowTimeShouldShowForMinShowTime(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	dialog := delayedprogress.NewDelayedProgressDialog(looper)
	dialog.SetMinDelay(500)
	dialog.SetMinShowTime(1000)
	dialog.Show()
	assert.False(t, dialog.IsShowing())
	looper.IdleFor(500)
	assert.True(t, dialog.IsShowing())
	looper.IdleFor(200)
	dialog.Dismiss()
	assert.True(t, dialog.IsShowing())
	looper.IdleFor(799)
	assert.True(t, dialog.IsShowing())
	looper.IdleFor(1)
	assert.False(t, dialog.IsShowing())
}

func TestDismissAfterMinShowTimeShouldDismissImmediately(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	dialog := delayedprogress.NewDelayedProgressDialog(looper)
	dialog.SetMinDelay(500)
	dialog.SetMinShowTime(1000)
	dialog.Show()
	assert.False(t, dialog.IsShowing())
	looper.IdleFor(500)
	assert.True(t, dialog.IsShowing())
	looper.IdleFor(1000)
	assert.True(t, dialog.IsShowing())
	dialog.Dismiss()
	assert.False(t, dialog.IsShowing())
}

func TestShowWithZeroMinDelayShowsImmediately(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	dialog := delayedprogress.NewDelayedProgressDialog(looper)
	dialog.SetMinDelay(0)
	dialog.SetMinShowTime(500)
	dialog.Show()
	assert.True(t, dialog.IsShowing())
	dialog.Dismiss()
	looper.IdleFor(500)
	assert.False(t, dialog.IsShowing())
}

func TestDismissWhenNeverShownNoOp(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	dialog := delayedprogress.NewDelayedProgressDialog(looper)
	dialog.SetMinDelay(1000)
	dialog.Show()
	assert.False(t, dialog.IsShowing())
	dialog.Dismiss()
	assert.False(t, dialog.IsShowing())
	looper.IdleFor(2000)
	assert.False(t, dialog.IsShowing())
}

func TestOnDetachedFromWindowRemovesCallbacksDialog(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	dialog := delayedprogress.NewDelayedProgressDialog(looper)
	dialog.Show()
	assert.Equal(t, 1, looper.CountPending())
	dialog.OnDetachedFromWindow()
	assert.Equal(t, 0, looper.CountPending())
	dialog.Dismiss()
	looper.IdleFor(2000)
	assert.False(t, dialog.IsShowing())
}

func TestSetMinShowTimeDialog(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	dialog := delayedprogress.NewDelayedProgressDialog(looper)
	dialog.SetMinShowTime(2000)
	dialog.SetMinDelay(0)
	dialog.Show()
	assert.True(t, dialog.IsShowing())
	dialog.Dismiss()
	looper.IdleFor(1999)
	assert.True(t, dialog.IsShowing())
	looper.IdleFor(1)
	assert.False(t, dialog.IsShowing())
}

func TestSetMinDelayDialog(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	dialog := delayedprogress.NewDelayedProgressDialog(looper)
	dialog.SetMinDelay(2000)
	dialog.SetMinShowTime(0)
	dialog.Show()
	assert.False(t, dialog.IsShowing())
	looper.IdleFor(1999)
	assert.False(t, dialog.IsShowing())
	looper.IdleFor(1)
	assert.True(t, dialog.IsShowing())
	dialog.Dismiss()
	assert.False(t, dialog.IsShowing())
}

func TestMultipleShowDismissCyclesDialog(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	dialog := delayedprogress.NewDelayedProgressDialog(looper)
	dialog.SetMinDelay(100)
	dialog.SetMinShowTime(200)
	// cycle 1
	dialog.Show()
	looper.IdleFor(50)
	dialog.Dismiss()
	looper.IdleFor(500)
	assert.False(t, dialog.IsShowing())
	// cycle 2
	dialog.Show()
	looper.IdleFor(100)
	assert.True(t, dialog.IsShowing())
	looper.IdleFor(200)
	assert.True(t, dialog.IsShowing())
	dialog.Dismiss()
	assert.False(t, dialog.IsShowing())
	// cycle 3
	dialog.Show()
	looper.IdleFor(100)
	assert.True(t, dialog.IsShowing())
	looper.IdleFor(100)
	assert.True(t, dialog.IsShowing())
	dialog.Dismiss()
	assert.True(t, dialog.IsShowing())
	looper.IdleFor(100)
	assert.False(t, dialog.IsShowing())
}