package public_tests

import "testing"

// Stub ParticleSystem tracking structure for public test.
type ParticleSystem struct {
	mCurrentTime int64
}

func (ps *ParticleSystem) Update(newTime int64) {
	ps.mCurrentTime = newTime
}

func TestParticleSystemDummyPublic_UpdateTimeProgressionPublic(t *testing.T) {
	ps := &ParticleSystem{}
	startTime := int64(1000)
	ps.mCurrentTime = startTime
	ps.Update(startTime + 300)
	if ps.mCurrentTime != 1300 {
		t.Errorf("Expected mCurrentTime=1300, got=%v", ps.mCurrentTime)
	}
}