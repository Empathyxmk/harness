package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"fenjuly_toggleexpandlayout/tests"
)

// DummyAnimator for public test (like Java DummyAnimator)
type DummyAnimator struct {
	tests.BaseAnimator
	prepared bool
}
func (a *DummyAnimator) Prepare(target *tests.View) {
	a.prepared = true
}
func (a *DummyAnimator) Animate(target *tests.View) {
	a.prepared = false
	a.Prepare(target)
}

func TestBaseAnimatorPublic_DurationsAreDifferent(t *testing.T) {
	anim := &DummyAnimator{}
	assert.Equal(t, tests.DefaultDuration, anim.GetDuration())
	anim.SetDuration(456)
	assert.Equal(t, 456, anim.GetDuration())
	anim.SetDuration(880)
	assert.Equal(t, 880, anim.GetDuration())
}

func TestBaseAnimatorPublic_AnimatorSet(t *testing.T) {
	anim := &DummyAnimator{}
	newSet := &tests.AnimatorSet{}
	anim.SetAnimatorSet(newSet)
	assert.Equal(t, newSet, anim.GetAnimatorSet())
}

func TestBaseAnimatorPublic_AnimatePrepares(t *testing.T) {
	anim := &DummyAnimator{}
	view := tests.NewMockView(11, 11)
	assert.False(t, anim.prepared)
	anim.Animate(view)
	assert.True(t, anim.prepared)
}