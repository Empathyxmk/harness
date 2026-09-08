package original

import "testing"

type ParticleField struct {
	particles []*Particle
}

func NewParticleField() *ParticleField {
	return &ParticleField{particles: []*Particle{}}
}

func (pf *ParticleField) SetParticles(particles []*Particle) {
	pf.particles = particles
}

func (pf *ParticleField) OnDraw() {
	// Simulate calling draw on all particles
	for _, p := range pf.particles {
		// No-op for test double
	}
}

func TestParticleField_Constructors(t *testing.T) {
	NewParticleField()
	NewParticleField() // AttributeSet params skipped in Go
	NewParticleField() // Style param skipped in Go
}

func TestParticleField_SetParticlesAndOnDraw(t *testing.T) {
	pf := NewParticleField()
	particle1 := &Particle{}
	particle2 := &Particle{}
	particles := []*Particle{particle1, particle2}
	pf.SetParticles(particles)
	pf.OnDraw() // would call draw on all particles
}