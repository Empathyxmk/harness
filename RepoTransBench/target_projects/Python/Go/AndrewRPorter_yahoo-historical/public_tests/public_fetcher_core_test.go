package public_tests

import (
	"errors"
	"fmt"
	"strings"
	"testing"
	"time"
	"yahoo-historical-go/yah"
)

func makePublicTimes() (int64, int64) {
	start := time.Date(2018, 2, 1, 0, 0, 0, 0, time.UTC).Unix()
	end := time.Date(2018, 2, 5, 0, 0, 0, 0, time.UTC).Unix()
	return start, end
}

func TestGetHistoricalPublic(t *testing.T) {
	start, end := makePublicTimes()
	f := yah.NewFetcher("GOOG", start, end)
	f.MockGet = func(kind string, asDataFrame bool) (interface{}, error) {
		return "open,close\n5,6\n7,8", nil
	}
	res, err := f.GetHistorical(false)
	if err != nil {
		t.Fatalf("GetHistorical returned error: %v", err)
	}
	if !strings.Contains(fmt.Sprintf("%v", res), "open") {
		t.Errorf("Expected 'open' in result")
	}
}

func TestReprStrPublic(t *testing.T) {
	start, end := makePublicTimes()
	f := yah.NewFetcher("GOOG", start, end)
	r := f.String()
	s := fmt.Sprintf("%v", f)
	if !strings.Contains(r, "Fetcher") || !strings.Contains(r, "GOOG") {
		t.Errorf("repr does not contain Fetcher or GOOG")
	}
	if !strings.Contains(s, "Fetcher") || !strings.Contains(s, "GOOG") {
		t.Errorf("string does not contain Fetcher or GOOG")
	}
}

func TestGetHistoryWithKwargsPublic(t *testing.T) {
	start, end := makePublicTimes()
	f := yah.NewFetcher("GOOG", start, end)
	f.MockGet = func(kind string, asDataFrame bool) (interface{}, error) {
		return "public_test", nil
	}
	res, err := f.GetHistorical(false)
	if err != nil {
		t.Fatalf("GetHistorical returned error: %v", err)
	}
	if res != "public_test" {
		t.Errorf("Expected public_test, got %v", res)
	}
}

func TestGetDividendAndSplitPublic(t *testing.T) {
	start, end := makePublicTimes()
	f := yah.NewFetcher("GOOG", start, end)
	if f.HasGetDividend() {
		if _, err := f.CallGetDividend(); err == nil {
			t.Error("Expected Exception calling GetDividend (as in public Python test)")
		}
		if _, err := f.CallGetSplit(); err == nil {
			t.Error("Expected Exception calling GetSplit")
		}
	} else {
		if _, err := f.CallGetDividend(); err == nil {
			t.Error("Expected AttributeError (method not found) calling GetDividend")
		}
		if _, err := f.CallGetSplit(); err == nil {
			t.Error("Expected AttributeError (method not found) calling GetSplit")
		}
	}
}

func TestKeyErrorPublic(t *testing.T) {
	start, end := makePublicTimes()
	f := yah.NewFetcher("GOOG", start, end)
	f.MockGet = func(kind string, asDataFrame bool) (interface{}, error) {
		return nil, errors.New("fail-public")
	}
	_, err := f.GetHistorical(true)
	if err == nil {
		t.Error("Expected KeyError (simulated), got nil")
	}
}

func TestWrongTickerPublic(t *testing.T) {
	start := time.Date(2019, 3, 4, 0, 0, 0, 0, time.UTC).Unix()
	end := time.Date(2019, 3, 5, 0, 0, 0, 0, time.UTC).Unix()
	f := yah.NewFetcher("!!!", start, end)
	_, err := f.GetHistorical(true)
	if err == nil {
		t.Error("Expected error for invalid ticker !!!, got nil")
	}
}