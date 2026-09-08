package original

import (
	"errors"
	"strings"
	"testing"
	"time"
	"yahoo-historical-go/yah"
)

func makeTestTimes() (int64, int64) {
	start := time.Date(2017, 1, 1, 0, 0, 0, 0, time.UTC).Unix()
	end := time.Date(2017, 1, 4, 0, 0, 0, 0, time.UTC).Unix()
	return start, end
}

func mockGetHistorical(self *yah.Fetcher, kind string, asDataFrame bool) (interface{}, error) {
	if asDataFrame {
		// Dummy equivalent: a struct with GetItem
		return &dummyDf{}, nil
	}
	return "col1,col2\n1,2\n3,4", nil
}

type dummyDf struct{}

func (d *dummyDf) GetItem(key string) []int {
	return []int{1, 2, 3}
}

func TestGetNoDataFrame(t *testing.T) {
	start, end := makeTestTimes()
	f := yah.NewFetcher("AAPL", start, end)
	f.MockGet = func(kind string, asDataFrame bool) (interface{}, error) {
		return "col1,col2\n1,2\n3,4", nil
	}
	res, err := f.GetHistorical(false)
	if err != nil {
		t.Fatalf("Failed to get historical: %v", err)
	}
	if !strings.Contains(res.(string), "col1") {
		t.Errorf("Expected 'col1' in data")
	}
}

func TestGetWithLowercase(t *testing.T) {
	start, end := makeTestTimes()
	f := yah.NewFetcher("aapl", start, end)
	f.MockGet = mockGetHistorical
	data, err := f.GetHistorical(true)
	if err != nil {
		t.Fatalf("Failed: %v", err)
	}
	if _, ok := data.(*dummyDf); !ok {
		t.Errorf("Expected dummyDf result")
	}
}

func TestGetHistorical_Fetch(t *testing.T) {
	start, end := makeTestTimes()
	f := yah.NewFetcher("AAPL", start, end)
	f.MockGet = mockGetHistorical
	data, err := f.GetHistorical(true)
	if err != nil {
		t.Fatalf("Failed: %v", err)
	}
	if _, ok := data.(*dummyDf); !ok {
		t.Errorf("Expected dummyDf result")
	}
}

func TestInvalidDate(t *testing.T) {
	start, end := makeTestTimes()
	f := yah.NewFetcher("AAPL", start, end)
	f.MockGet = mockGetHistorical
	invalidStart := interface{}("invalid_date")
	// Simulate instantiating fetcher with invalid date
	f2 := yah.NewFetcher("AAPL", invalidStart, end)
	f2.MockGet = mockGetHistorical
	_, err := f2.GetHistorical(true)
	if err == nil {
		t.Errorf("Expected error with invalid date type, got nil")
	}
}

func TestFetcherWithFloatDates(t *testing.T) {
	start, end := float64(time.Date(2017, 1, 1, 0, 0, 0, 0, time.UTC).Unix()), float64(time.Date(2017, 1, 4, 0, 0, 0, 0, time.UTC).Unix())
	f := yah.NewFetcher("AAPL", start, end)
	f.MockGet = mockGetHistorical
	data, err := f.GetHistorical(true)
	if err != nil {
		t.Fatalf("GetHistorical: %v", err)
	}
	if _, ok := data.(*dummyDf); !ok {
		t.Errorf("Expected dummyDf for float dates")
	}
}