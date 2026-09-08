package public_tests

import (
	"testing"
	"yahoo-historical-go/yah"
)

func TestImportFetcherPublic(t *testing.T) {
	f := yah.NewFetcher("msft", 1650000000, 1650001000)
	if f == nil {
		t.Fatal("Fetcher instance is nil")
	}
	if !f.HasGetHistorical() {
		t.Errorf("Fetcher does not have method GetHistorical")
	}
}