package original

import "testing"

type ParticleModifierFunc func(p *Particle, ms int64)

func (f ParticleModifierFunc) Apply(p *Particle, ms int64) {
	f(p, ms)
}

func TestParticleModifier_ApplyNoop(t *testing.T) {
	p := &Particle{}
	modifier := ParticleModifierFunc(func(p *Particle, ms int64) {})
	modifier.Apply(p, 10)
}