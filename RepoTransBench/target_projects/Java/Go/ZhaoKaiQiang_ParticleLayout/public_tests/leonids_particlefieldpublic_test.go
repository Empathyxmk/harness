package public_tests

import "testing"

type Particle struct {
	mCurrentX float32
	mCurrentY float32
}

type ParticleField struct {
	particles []*Particle
}

func (pf *ParticleField) SetParticles(p []*Particle) {
	pf.particles = p
}

func TestParticleFieldPublic_SetParticlesPublic(t *testing.T) {
	field := &ParticleField{}
	particles := []*Particle{}
	p := &Particle{}
	particles = append(particles, p)
	field.SetParticles(particles)
	if field == nil {
		t.Error("field was nil")
	}
	if len(particles) != 1 {
		t.Errorf("Expected 1 particle, got %d", len(particles))
	}
}