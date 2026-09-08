package original

import (
	"testing"
	"yahoo-historical-go/yah"
)

func TestImportFetcher(t *testing.T) {
	f := yah.NewFetcher("aapl", 1600000000, 1600001000)
	if f == nil {
		t.Fatal("Fetcher instance is nil")
	}
	if !f.HasGetHistorical() {
		t.Errorf("Fetcher does not have method GetHistorical")
	}
}