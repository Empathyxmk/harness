package public_tests

import "testing"

// Minimal Particle type for public tests, with directly settable fields.
type Particle struct {
	mCurrentX float32
	mCurrentY float32
}

func TestParticlePublic_InitialValuesAreSetPublic(t *testing.T) {
	p := &Particle{}
	p.mCurrentX = 15.0
	p.mCurrentY = 25.0
	const delta = 0.01
	if diff := p.mCurrentX - 15.0; diff < -delta || diff > delta {
		t.Errorf("Expected mCurrentX=15, got=%.2f", p.mCurrentX)
	}
	if diff := p.mCurrentY - 25.0; diff < -delta || diff > delta {
		t.Errorf("Expected mCurrentY=25, got=%.2f", p.mCurrentY)
	}
}