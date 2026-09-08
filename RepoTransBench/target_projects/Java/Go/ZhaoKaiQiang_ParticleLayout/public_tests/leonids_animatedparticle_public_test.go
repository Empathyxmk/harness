package public_tests

import "testing"

type AnimatedParticle struct {
	mLifetime int
}

func TestAnimatedParticlePublic_AnimationValuesPublic(t *testing.T) {
	particle := &AnimatedParticle{}
	particle.mLifetime = 3000
	if particle.mLifetime != 3000 {
		t.Errorf("Expected mLifetime=3000, got=%v", particle.mLifetime)
	}
}