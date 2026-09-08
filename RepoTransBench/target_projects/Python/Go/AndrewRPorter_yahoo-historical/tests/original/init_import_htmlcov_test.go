package original

import (
	"testing"
	"yahoo-historical-go/yah"
)

// This file corresponds to htmlcov/d_a44f0ac069e85531_test_init_import_py.html

func TestImportFetcherHtmlCov(t *testing.T) {
	f := yah.NewFetcher("aapl", 1600000000, 1600001000)
	if f == nil {
		t.Fatal("Fetcher instance is nil")
	}
	if !f.HasGetHistorical() {
		t.Errorf("Fetcher does not have method GetHistorical")
	}
}