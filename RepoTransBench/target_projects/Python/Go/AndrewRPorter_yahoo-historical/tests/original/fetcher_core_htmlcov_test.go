package original

import (
	"errors"
	"fmt"
	"strings"
	"testing"
	"time"
	"yahoo-historical-go/yah"
)

// This file corresponds to htmlcov/z_a44f0ac069e85531_test_fetcher_core_py.html

func makeTimesHtmlCov() (int64, int64) {
	start := time.Date(2017, 1, 1, 0, 0, 0, 0, time.UTC).Unix()
	end := time.Date(2017, 1, 4, 0, 0, 0, 0, time.UTC).Unix()
	return start, end
}

func TestGetHistoricalHtmlCov(t *testing.T) {
	start, end := makeTimesHtmlCov()
	f := yah.NewFetcher("AAPL", start, end)
	f.MockGet = func(kind string, asDataFrame bool) (interface{}, error) {
		return "col1,col2\n1,2\n3,4", nil
	}
	res, err := f.GetHistorical(false)
	if err != nil {
		t.Fatalf("GetHistorical (patched) returned error: %v", err)
	}
	if !strings.Contains(fmt.Sprintf("%v", res), "col1") {
		t.Errorf("Expected 'col1' in result, got: %v", res)
	}
}

func TestReprStrHtmlCov(t *testing.T) {
	start, end := makeTimesHtmlCov()
	f := yah.NewFetcher("AAPL", start, end)
	r := f.String()
	s := fmt.Sprintf("%v", f)
	if !strings.Contains(r, "Fetcher") {
		t.Errorf("Expected 'Fetcher' in repr: %s", r)
	}
	if !strings.Contains(s, "Fetcher") {
		t.Errorf("Expected 'Fetcher' in string: %s", s)
	}
}

func TestGetHistoryWithKwargsHtmlCov(t *testing.T) {
	start, end := makeTimesHtmlCov()
	f := yah.NewFetcher("AAPL", start, end)
	f.MockGet = func(kind string, asDataFrame bool) (interface{}, error) {
		return "test", nil
	}
	res, err := f.GetHistorical(false)
	if err != nil {
		t.Fatalf("GetHistorical kwarg: %v", err)
	}
	if res != "test" {
		t.Errorf("Expected result 'test', got: %v", res)
	}
}

func TestGetDividendAndSplitHtmlCov(t *testing.T) {
	start, end := makeTimesHtmlCov()
	f := yah.NewFetcher("AAPL", start, end)
	if f.HasGetDividend() || f.HasGetSplit() {
		t.Fatal("Fetcher unexpectedly has GetDividend or GetSplit method")
	}
	if _, err := f.CallGetDividend(); err == nil {
		t.Error("Expected error calling GetDividend, got nil")
	}
	if _, err := f.CallGetSplit(); err == nil {
		t.Error("Expected error calling GetSplit, got nil")
	}
}

func TestKeyErrorHtmlCov(t *testing.T) {
	start, end := makeTimesHtmlCov()
	f := yah.NewFetcher("AAPL", start, end)
	f.MockGet = func(kind string, asDataFrame bool) (interface{}, error) {
		return nil, errors.New("fail")
	}
	_, err := f.GetHistorical(true)
	if err == nil {
		t.Error("Expected error (KeyError), got nil")
	}
}

func TestWrongTickerHtmlCov(t *testing.T) {
	start := time.Date(2020, 1, 1, 0, 0, 0, 0, time.UTC).Unix()
	end := time.Date(2020, 1, 2, 0, 0, 0, 0, time.UTC).Unix()
	f := yah.NewFetcher("", start, end)
	_, err := f.GetHistorical(true)
	if err == nil {
		t.Error("Expected error with empty ticker, got nil")
	}
}