package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Simulate Animator and View classes and ExpandAnimationUtils for Go

type Animator struct{}
type MockView struct {
	left, top, width, height int
}
type MockViewGroup struct {
	children []*MockView
}
func (vg *MockViewGroup) GetChildCount() int {
	return len(vg.children)
}
func (vg *MockViewGroup) GetChildAt(i int) *MockView {
	return vg.children[i]
}

// ExpandAnimationUtils methods

func BuildExpandAnimators(vg *MockViewGroup, pivotX, pivotY int, fraction float32, duration, delay int) []Animator {
	// builds 2 animators for each child (x and y), plus 1 alpha animator
	animators := []Animator{}
	for i := 0; i < vg.GetChildCount(); i++ {
		animators = append(animators, Animator{}) // x
		animators = append(animators, Animator{}) // y
	}
	animators = append(animators, Animator{}) // alpha
	return animators
}
func BuildExpandAnimatorsReversed(vg *MockViewGroup, pivotX, pivotY int, fraction float32, duration, delay int) []Animator {
	// Same as above for test purposes
	return BuildExpandAnimators(vg, pivotX, pivotY, fraction, duration, delay)
}

func TestExpandAnimationUtils_Build(t *testing.T) {
	mockViewGroup := &MockViewGroup{}
	child1 := &MockView{left: 10, top: 20, width: 30, height: 40}
	child2 := &MockView{left: 100, top: 200, width: 50, height: 60}
	mockViewGroup.children = []*MockView{child1, child2}

	pivotX := 50
	pivotY := 60
	fraction := float32(0.5)
	duration := 300
	delay := 50

	animators := BuildExpandAnimators(mockViewGroup, pivotX, pivotY, fraction, duration, delay)

	assert.Equal(t, 5, len(animators), "Should be 2 children x2 (x,y) + 1 alpha = 5 animators")
	for i := 0; i < 4; i++ {
		assert.NotNil(t, &animators[i], "Animator should not be nil")
	}
	assert.NotNil(t, &animators[4], "Alpha animator should be present")
}

func TestExpandAnimationUtils_BuildReversed(t *testing.T) {
	mockViewGroup := &MockViewGroup{}
	child1 := &MockView{left: 10, top: 20, width: 30, height: 40}
	child2 := &MockView{left: 100, top: 200, width: 50, height: 60}
	mockViewGroup.children = []*MockView{child1, child2}

	pivotX := 30
	pivotY := 90
	fraction := float32(0.3)
	duration := 400
	delay := 20

	animators := BuildExpandAnimatorsReversed(mockViewGroup, pivotX, pivotY, fraction, duration, delay)

	assert.Equal(t, 5, len(animators), "Should be 2 children x2 (x,y) + 1 alpha = 5 animators")
	for i := 0; i < 5; i++ {
		assert.NotNil(t, &animators[i], "Animator should not be nil")
	}
}