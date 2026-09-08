package tests

import (
	"testing"
	"dlew_rxjava_multiple_sources_sample/dlew"
	. "dlew_rxjava_multiple_sources_sample/tests"
)

func TestSources_MemoryInitialNull(t *testing.T) {
	sources := dlew.NewSources()
	ch := sources.Memory()
	AssertFirstIsNil(t, ch)
	AssertCompleted(t, ch)
}

func TestSources_DiskInitialNull(t *testing.T) {
	sources := dlew.NewSources()
	ch := sources.Disk()
	AssertFirstIsNil(t, ch)
	AssertCompleted(t, ch)
}

func TestSources_NetworkReturnsDataAndCachesToDiskAndMemory(t *testing.T) {
	sources := dlew.NewSources()
	<-sources.Network() // populate

	mem := sources.Memory()
	AssertValueCount(t, mem, 1)
	disk := sources.Disk()
	AssertValueCount(t, disk, 1)
}

func TestSources_ClearMemory(t *testing.T) {
	sources := dlew.NewSources()
	sources.ClearMemory()
	ch := sources.Memory()
	AssertFirstIsNil(t, ch)
}