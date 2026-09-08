package original

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"tasomaniac_delayedprogress/delayedprogress"
)

func TestConstructors(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar1 := delayedprogress.NewDelayedProgressBar(looper)
	assert.False(t, bar1.IsShown(), "Bar1 is not shown initially")
	bar2 := delayedprogress.NewDelayedProgressBar(looper)
	assert.False(t, bar2.IsShown(), "Bar2 is not shown initially")
}

func TestShowNoDelay(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	bar.Show()
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
	looper.IdleFor(500)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	assert.InDelta(t, 0.0, float64(bar.GetAlpha()), 0.001)
}

func TestShowWithAnimation(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	bar.SetAlpha(0.0)
	assert.InDelta(t, 0.0, float64(bar.GetAlpha()), 0.001)
	bar.ShowAnim(true)
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
	looper.IdleFor(500)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	assert.InDelta(t, 1.0, float64(bar.GetAlpha()), 0.001)
}

func TestShowWithAnimationAndEndAction(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	called := false
	bar.SetAlpha(0.0)
	bar.ShowAnimWithEnd(true, func() { called = true })
	looper.IdleFor(500)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	assert.True(t, called, "EndAction should be run")
}

func TestHideBeforeMinDelayShouldNotShow(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	bar.Show()
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
	looper.IdleFor(200)
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
	bar.Hide()
	looper.IdleFor(500)
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
}

func TestHideAfterMinDelayButBeforeMinShowTimeShouldShowForMinShowTime(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	bar.Show()
	looper.IdleFor(500)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	looper.IdleFor(200)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	bar.Hide()
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	looper.IdleFor(299)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	looper.IdleFor(1)
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
}

func TestHideAfterMinShowTimeShouldHideImmediately(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	bar.Show()
	looper.IdleFor(500)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	looper.IdleFor(500)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	bar.Hide()
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
}

func TestHideWithAnimationHidesWithFade(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	bar.Show()
	looper.IdleFor(500)
	bar.SetAlpha(1.0)
	bar.HideAnim(true)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	looper.IdleFor(500)
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
	assert.InDelta(t, 0.0, float64(bar.GetAlpha()), 0.001)
}

func TestHideWithAnimationAndEndActionHidesWithFadeAndRunsEndAction(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	called := false
	bar.Show()
	looper.IdleFor(500)
	bar.SetAlpha(1.0)
	bar.HideAnimWithEnd(true, func() { called = true })
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	looper.IdleFor(500)
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
	assert.True(t, called, "EndAction called")
}

func TestOnDetachedFromWindowRemovesCallbacks(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	bar.Show()
	assert.Equal(t, 1, looper.CountPending())
	bar.OnDetachedFromWindow()
	assert.Equal(t, 0, looper.CountPending())
	bar.Show()
	looper.IdleFor(500)
	bar.Hide()
	assert.Equal(t, 1, looper.CountPending())
	bar.OnDetachedFromWindow()
	assert.Equal(t, 0, looper.CountPending())
}

func TestImmediateHideWhenNeverShown(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	bar.Hide()
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
}

func TestShowAndHideCalledMultipleTimes(t *testing.T) {
	looper := delayedprogress.NewLooperMock()
	bar := delayedprogress.NewDelayedProgressBar(looper)
	bar.Show()
	looper.IdleFor(100)
	bar.Hide()
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
	bar.Show()
	looper.IdleFor(600)
	assert.Equal(t, delayedprogress.ViewVisible, bar.GetVisibility())
	bar.Hide()
	assert.Equal(t, delayedprogress.ViewGone, bar.GetVisibility())
}