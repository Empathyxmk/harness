package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"tasomaniac_delayedprogress/delayedprogress"
)

func TestConstructorsPublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar1 := delayedprogress.NewDelayedProgressBar(looper)
	assert.False(t, bar1.IsShown(), "Bar1 is not shown initially")
	bar2 := delayedprogress.NewDelayedProgressBar(looper)
	assert.False(t, bar2.IsShown(), "Bar2 is not shown initially")
}

func TestShowNoDelayPublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	bar.SetMinDelay(300)
	bar.SetMinShowTime(700)
	bar.Show()
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
	looper.IdleFor(300)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	assert.InDelta(t, 0.0, float64(bar.GetAlpha()), 0.001)
}

func TestShowWithAnimationPublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	bar.SetAlpha(0.0)
	bar.SetMinDelay(350)
	bar.ShowAnim(true)
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
	looper.IdleFor(350)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	assert.InDelta(t, 1.0, float64(bar.GetAlpha()), 0.001)
}

func TestShowWithAnimationAndEndActionPublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	called := false
	bar.SetAlpha(0.0)
	bar.SetMinDelay(250)
	bar.ShowAnimWithEnd(true, func() { called = true })
	looper.IdleFor(250)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	assert.True(t, called, "EndAction should be run")
}

func TestHideBeforeMinDelayShouldNotShowPublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	bar.SetMinDelay(400)
	bar.Show()
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
	looper.IdleFor(150)
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
	bar.Hide()
	looper.IdleFor(400)
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
}

func TestHideAfterMinDelayButBeforeMinShowTimePublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	bar.SetMinDelay(350)
	bar.SetMinShowTime(650)
	bar.Show()
	looper.IdleFor(350)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	looper.IdleFor(250)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	bar.Hide()
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	looper.IdleFor(399)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	looper.IdleFor(1)
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
}

func TestHideAfterMinShowTimeShouldHideImmediatelyPublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	bar.SetMinDelay(280)
	bar.SetMinShowTime(420)
	bar.Show()
	looper.IdleFor(280)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	looper.IdleFor(420)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	bar.Hide()
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
}

func TestHideWithAnimationHidesWithFadePublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	bar.SetMinDelay(220)
	bar.SetMinShowTime(330)
	bar.Show()
	looper.IdleFor(220)
	bar.SetAlpha(1.0)
	bar.HideAnim(true)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	looper.IdleFor(330)
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
	assert.InDelta(t, 0.0, float64(bar.GetAlpha()), 0.001)
}

func TestHideWithAnimationAndEndActionHidesWithFadeAndRunsEndActionPublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	called := false
	bar.SetMinDelay(420)
	bar.SetMinShowTime(350)
	bar.Show()
	looper.IdleFor(420)
	bar.SetAlpha(1.0)
	bar.HideAnimWithEnd(true, func() { called = true })
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	looper.IdleFor(350)
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
	assert.True(t, called, "EndAction called")
}

func TestOnDetachedFromWindowRemovesCallbacksPublic(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	bar.SetMinDelay(290)
	bar.Show()
	assert.Equal(t, 1, looper.CountPending())
	bar.OnDetachedFromWindow()
	assert.Equal(t, 0, looper.CountPending())
	bar.SetMinDelay(310)
	bar.Show()
	looper.IdleFor(310)
	bar.Hide()
	assert.Equal(t, 1, looper.CountPending())
	bar.OnDetachedFromWindow()
	assert.Equal(t, 0, looper.CountPending())
}