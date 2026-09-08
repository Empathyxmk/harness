package public_tests

import (
	"testing"
)

type SimplePauseDetectorPublic struct {
	resolutionMillis int
	verbose          bool
}

func NewSimplePauseDetectorPublic(res, threadCount int) *SimplePauseDetectorPublic {
	return &SimplePauseDetectorPublic{resolutionMillis: res}
}
func (spd *SimplePauseDetectorPublic) getResolutionMillis() int {
	return spd.resolutionMillis
}
func (spd *SimplePauseDetectorPublic) setVerbose(v bool) {
	spd.verbose = v
}
func (spd *SimplePauseDetectorPublic) isVerbose() bool {
	return spd.verbose
}

func TestGetResolution(t *testing.T) {
	detector := NewSimplePauseDetectorPublic(10, 4)
	if detector.getResolutionMillis() != 10 {
		t.Errorf("expected 10, got %d", detector.getResolutionMillis())
	}
}

func TestSetVerbose(t *testing.T) {
	detector := NewSimplePauseDetectorPublic(3, 2)
	detector.setVerbose(true)
	if !detector.isVerbose() {
		t.Errorf("expected verbose true")
	}
	detector.setVerbose(false)
	if detector.isVerbose() {
		t.Errorf("expected verbose false")
	}
}