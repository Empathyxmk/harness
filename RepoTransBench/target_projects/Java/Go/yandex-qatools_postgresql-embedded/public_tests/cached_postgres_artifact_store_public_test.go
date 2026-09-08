package public_tests

import (
	"strings"
	"testing"
)

type DummyCache struct {
	fileName     string
	timesFetched int
}

func NewDummyCache(fileName string) *DummyCache {
	return &DummyCache{fileName: fileName}
}

func (c *DummyCache) Fetch() string {
	c.timesFetched++
	return "fetched_public_" + c.fileName
}

func (c *DummyCache) GetTimesFetched() int {
	return c.timesFetched
}

func TestFetchReturnsFileWithDifferentName(t *testing.T) {
	cache := NewDummyCache("pubfile-2211.txt")
	res := cache.Fetch()
	if !strings.Contains(res, "pubfile-2211.txt") {
		t.Errorf("Expected fetch result with pubfile-2211.txt, got '%s'", res)
	}
}

func TestFetchCountsTimesFetchedWithDifferentFile(t *testing.T) {
	cache := NewDummyCache("pubcache.data")
	cache.Fetch()
	cache.Fetch()
	if cache.GetTimesFetched() != 2 {
		t.Errorf("Expected timesFetched to be 2, got %d", cache.GetTimesFetched())
	}
}