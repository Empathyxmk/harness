package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// minimal stub replacing BaseAnimator in testutil
type testAnimator struct {
	BaseAnimator
	prepared bool
}

func (a *testAnimator) Prepare(target *View) {
	a.prepared = true
}

func (a *testAnimator) Animate(v *View) {
	a.prepared = false
	a.Prepare(v)
}

func TestBaseAnimator_DefaultDuration(t *testing.T) {
	anim := &testAnimator{}
	anim.duration = DefaultDuration
	assert.Equal(t, DefaultDuration, anim.GetDuration())
}

func TestBaseAnimator_SetAnimatorSet(t *testing.T) {
	anim := &testAnimator{}
	mySet := &AnimatorSet{}
	anim.SetAnimatorSet(mySet)
	assert.Equal(t, mySet, anim.GetAnimatorSet())
}

func TestBaseAnimator_SetGetDuration(t *testing.T) {
	anim := &testAnimator{}
	anim.SetDuration(500)
	assert.Equal(t, 500, anim.GetDuration())
}

func TestBaseAnimator_PrepareAndAnimate(t *testing.T) {
	anim := &testAnimator{}
	view := NewMockView(13, 13)
	anim.Animate(view)
	assert.True(t, anim.prepared)
}

type dummyListener struct{}
func (d *dummyListener) OnAnimationStart() {}
func (d *dummyListener) OnAnimationEnd()   {}
func (d *dummyListener) OnAnimationCancel() {}
func (d *dummyListener) OnAnimationRepeat() {}

func TestBaseAnimator_AddAnimatorListenerAndStart(t *testing.T) {
	anim := &testAnimator{}
	listener := &dummyListener{}
	anim.AddAnimatorListener(listener)
	anim.Start()
	// No exception expected
}