package tests

import (
	"testing"
	"dlew_rxjava_multiple_sources_sample/dlew"
	. "dlew_rxjava_multiple_sources_sample/tests"
	"time"
)

func TestSourcesBranch_MemoryWithFreshData(t *testing.T) {
	sources := dlew.NewSources()
	// Store a fresh Data in memory by simulating a network request
	<-sources.Network()
	ch := sources.Memory()
	AssertValueCount(t, ch, 1)
}

func TestSourcesBranch_DiskWithFreshData(t *testing.T) {
	sources := dlew.NewSources()
	<-sources.Network()
	ch := sources.Disk()
	AssertValueCount(t, ch, 1)
}

func TestSourcesBranch_NetworkMultipleRequests(t *testing.T) {
	sources := dlew.NewSources()
	data1 := <-sources.Network()
	data2 := <-sources.Network()
	ch := sources.Memory()
	AssertValueCount(t, ch, 1)
	if data1.Value == data2.Value {
		t.Errorf("expected network requests to yield different values, got %q twice", data1.Value)
	}
}

func TestSourcesBranch_LogSourceNullAndStale(t *testing.T) {
	sources := dlew.NewSources()

	input := make(chan *dlew.Data, 8)
	input <- nil
	input <- &dlew.Data{Value: "x", Timestamp: time.Now().UnixMilli() - 6000}
	input <- &dlew.Data{Value: "y", Timestamp: time.Now().UnixMilli()}
	close(input)

	out := sources.LogSource("UNITTEST")(input)
	AssertValueCount(t, out, 3)
}