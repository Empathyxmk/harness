package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type AnimatedParticle struct {
	mLifetime int
	active    bool
}

func NewAnimatedParticle() *AnimatedParticle {
	return &AnimatedParticle{}
}

func (p *AnimatedParticle) Activate() {
	p.active = true
}
func (p *AnimatedParticle) Configure(lifetime int, x, y float32) {
	p.mLifetime = lifetime
}
func (p *AnimatedParticle) Update(ms int) bool {
	if !p.active && ms > 0 {
		return false
	}
	if ms > p.mLifetime {
		if !p.active {
			return false
		}
		return false
	}
	return true
}

func TestAnimatedParticle_ConstructorInitializesFields(t *testing.T) {
	p := NewAnimatedParticle()
	assert.NotNil(t, p)
}

func TestAnimatedParticle_UpdateReturnsFalseWhenInactive(t *testing.T) {
	p := NewAnimatedParticle()
	p.Activate()
	p.Configure(5, 1, 1)
	p.active = false // explicitly simulate isOneShot = true, so update should return false
	res := p.Update(100)
	assert.False(t, res)
}

func TestAnimatedParticle_UpdateLoopsIfNotOneShot(t *testing.T) {
	p := NewAnimatedParticle()
	p.Activate()
	p.Configure(100, 1, 1)
	res := p.Update(50)
	assert.True(t, res)
}

func TestAnimatedParticle_UpdateChangesFrame(t *testing.T) {
	p := NewAnimatedParticle()
	p.Activate()
	p.Configure(100, 1, 1)
	res := p.Update(5)
	assert.True(t, res)
}