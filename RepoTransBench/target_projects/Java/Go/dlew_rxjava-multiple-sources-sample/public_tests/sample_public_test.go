package public_tests

import (
	"testing"
	"dlew_rxjava_multiple_sources_sample/dlew"
)

func TestSample_MainRunsPublic(t *testing.T) {
	dlew.Sample{}.Sleep(10) // Simulate main's sleep
}