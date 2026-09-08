package public_tests

import (
	"testing"
	"time"
	"dlew_rxjava_multiple_sources_sample/dlew"
)

func TestData_IsUpToDate_whenFreshPublic(t *testing.T) {
	data := dlew.NewData("public")
	if !data.IsUpToDate() {
		t.Errorf("expected fresh data to be up-to-date (public)")
	}
}

func TestData_IsUpToDate_whenStalePublic(t *testing.T) {
	data := dlew.NewData("anotherPublic")
	time.Sleep(5200 * time.Millisecond)
	if data.IsUpToDate() {
		t.Errorf("expected stale data to NOT be up-to-date (public)")
	}
}

func TestData_ValueAndTimestampPublic(t *testing.T) {
	data := dlew.NewData("differentSample")
	if data.Value != "differentSample" {
		t.Errorf("expected value 'differentSample', got %q", data.Value)
	}
	if data.Timestamp > time.Now().UnixMilli() {
		t.Errorf("timestamp should not be from the future (public)")
	}
}