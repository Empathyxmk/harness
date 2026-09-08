package tests

import (
	"testing"
	"time"

	"dlew_rxjava_multiple_sources_sample/dlew"
)

func TestData_IsUpToDate_whenFresh(t *testing.T) {
	data := dlew.NewData("test")
	if !data.IsUpToDate() {
		t.Errorf("expected fresh data to be up-to-date")
	}
}

func TestData_IsUpToDate_whenStale(t *testing.T) {
	data := dlew.NewData("test")
	time.Sleep(5100 * time.Millisecond) // ensure staleness, as STALE_MS = 5000
	if data.IsUpToDate() {
		t.Errorf("expected stale data to NOT be up-to-date")
	}
}

func TestData_ValueAndTimestamp(t *testing.T) {
	data := dlew.NewData("sample")
	if data.Value != "sample" {
		t.Errorf("expected value 'sample', got %q", data.Value)
	}
	if data.Timestamp > time.Now().UnixMilli() {
		t.Errorf("timestamp should not be from the future")
	}
}