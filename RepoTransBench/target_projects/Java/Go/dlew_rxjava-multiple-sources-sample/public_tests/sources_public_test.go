package public_tests

import (
	"testing"
	"dlew_rxjava_multiple_sources_sample/dlew"
	. "dlew_rxjava_multiple_sources_sample/tests"
)

func TestSources_MemoryInitialNullPublic(t *testing.T) {
	sources := dlew.NewSources()
	ch := sources.Memory()
	AssertFirstIsNil(t, ch)
	AssertCompleted(t, ch)
}

func TestSources_DiskInitialNullPublic(t *testing.T) {
	sources := dlew.NewSources()
	ch := sources.Disk()
	AssertFirstIsNil(t, ch)
	AssertCompleted(t, ch)
}

func TestSources_NetworkReturnsDataAndCachesToDiskAndMemoryPublic(t *testing.T) {
	sources := dlew.NewSources()
	<-sources.Network()
	mem := sources.Memory()
	AssertValueCount(t, mem, 1)
	disk := sources.Disk()
	AssertValueCount(t, disk, 1)
}

func TestSources_ClearMemoryPublic(t *testing.T) {
	sources := dlew.NewSources()
	<-sources.Network() // fill memory
	sources.ClearMemory()
	ch := sources.Memory()
	AssertFirstIsNil(t, ch)
}