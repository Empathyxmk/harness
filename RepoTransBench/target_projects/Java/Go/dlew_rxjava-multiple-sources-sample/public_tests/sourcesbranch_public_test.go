package public_tests

import (
	"testing"
	"dlew_rxjava_multiple_sources_sample/dlew"
	. "dlew_rxjava_multiple_sources_sample/tests"
	"time"
)

func TestSourcesBranch_MemoryWithFreshDataPublic(t *testing.T) {
	sources := dlew.NewSources()
	<-sources.Network()
	ch := sources.Memory()
	AssertValueCount(t, ch, 1)
}

func TestSourcesBranch_DiskWithFreshDataPublic(t *testing.T) {
	sources := dlew.NewSources()
	<-sources.Network()
	ch := sources.Disk()
	AssertValueCount(t, ch, 1)
}

func TestSourcesBranch_NetworkMultipleRequestsPublic(t *testing.T) {
	sources := dlew.NewSources()
	dataA := <-sources.Network()
	dataB := <-sources.Network()
	ch := sources.Memory()
	AssertValueCount(t, ch, 1)
	if dataA.Value == dataB.Value {
		t.Errorf("expected network request values to differ (public)")
	}
}

func TestSourcesBranch_LogSourceNullAndStalePublic(t *testing.T) {
	sources := dlew.NewSources()

	input := make(chan *dlew.Data, 8)
	input <- nil
	input <- &dlew.Data{Value: "abc", Timestamp: time.Now().UnixMilli() - 6000}
	input <- &dlew.Data{Value: "def", Timestamp: time.Now().UnixMilli()}
	close(input)

	out := sources.LogSource("UNITTEST_PUBLIC")(input)
	AssertValueCount(t, out, 3)
}