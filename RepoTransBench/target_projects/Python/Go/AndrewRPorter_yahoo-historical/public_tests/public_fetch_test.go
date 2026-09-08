package public_tests

import (
	"strings"
	"testing"
	"yahoo-historical-go/yah"
)

func TestFetcherCreateURLPublic(t *testing.T) {
	f := yah.NewFetcher("NFLX", 1500000000, 1500500000)
	url := f.CreateURL("history")
	if !strings.Contains(url, "NFLX") {
		t.Error("Expected 'NFLX' in URL")
	}
	if !strings.Contains(url, "history") {
		t.Error("Expected 'history' in URL")
	}
}

func TestFetcherInvalidIntervalPublic(t *testing.T) {
	f := yah.NewFetcher("NFLX", 1510000000, 1510500000)
	f.SetInterval("8h")
	_, err := f.GetHistorical(true)
	if err == nil {
		t.Error("Expected ValueError for unsupported interval")
	}
}

func TestFetcherGetHistoricalDataFramePublic(t *testing.T) {
	dataCSV := "a,b\n1,2\n3,4"
	var fakeResp yah.FakeResponse
	fakeResp.Content = []byte(dataCSV)

	f := yah.NewFetcher("AMZN", 1550000000, 1550600000)
	f.CreateURLFunc = func(event string) string {
		return "http://test-url/"
	}
	f.RequestGetFunc = func(url string, headers map[string]string) yah.FakeResponse {
		return fakeResp
	}
	df, err := f.GetHistorical(true)
	if err != nil {
		t.Fatalf("GetHistorical returned error: %v", err)
	}
	gdf, ok := df.(yah.GoDataFrame)
	if !ok {
		t.Fatalf("Result is not GoDataFrame: %T", df)
	}
	if !gdf.HasColumns("a", "b") {
		t.Errorf("Expected columns 'a' and 'b'")
	}
	if gdf.Cell(0, "a") != 1 {
		t.Errorf("Expected first row 'a' to be 1, got %v", gdf.Cell(0, "a"))
	}
}