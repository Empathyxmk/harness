package public_tests

import "testing"

type Particle struct {
	mCurrentY float32
}

type ParticleModifier interface {
	Apply(p *Particle, ms int64)
}

type myModifier struct{}

func (m *myModifier) Apply(p *Particle, ms int64) {
	p.mCurrentY = 44.0
}

func TestParticleModifierPublic_ModifyPublic(t *testing.T) {
	m := &myModifier{}
	p := &Particle{}
	m.Apply(p, 100)
	const delta = 0.001
	if diff := p.mCurrentY - 44.0; diff < -delta || diff > delta {
		t.Errorf("Expected mCurrentY=44.0, got=%v", p.mCurrentY)
	}
}