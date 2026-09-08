package original

import (
	"encoding/json"
	"reflect"
	"testing"

	mftool "NayakwadiS_mftool"
)

func countEqual(a, b map[string]interface{}) bool {
	// Quick map equality check: all keys & values must be equal
	if len(a) != len(b) {
		return false
	}
	for k, v := range a {
		if v2, ok := b[k]; !ok || !reflect.DeepEqual(v, v2) {
			return false
		}
	}
	return true
}

func TestGetSchemeCodes(t *testing.T) {
	mft := mftool.NewMftool()
	sc := mft.GetSchemeCodes()
	if sc == nil {
		t.Fatal("GetSchemeCodes() returned nil")
	}
	if reflect.TypeOf(sc).Kind() != reflect.Map {
		t.Errorf("Expected map for GetSchemeCodes")
	}
	scJson := mft.GetSchemeCodesAsJSON()
	if reflect.TypeOf(scJson).Kind() != reflect.String {
		t.Errorf("Expected JSON string")
	}
	// Check json round-trip
	var scMap map[string]interface{}
	if err := json.Unmarshal([]byte(scJson), &scMap); err != nil {
		t.Fatalf("JSON Unmarshal failed: %v", err)
	}
	if !countEqual(sc, scMap) {
		t.Errorf("Original map and unmarshaled map differ")
	}
	result := mft.GetAvailableSchemes("ICICI")
	// Get first key
	for _, v := range result {
		if v == "Axis" {
			t.Errorf("Result value should not be 'Axis' (bad test logic possible?)")
		}
		break
	}
}

func TestIsValidCode(t *testing.T) {
	mft := mftool.NewMftool()
	code := "119598"
	if !mft.IsValidCode(code) {
		t.Errorf("Code %s should be valid", code)
	}
}

func TestNegativeIsValidCode(t *testing.T) {
	mft := mftool.NewMftool()
	code := "1195"
	if mft.IsValidCode(code) {
		t.Errorf("Code %s should be invalid", code)
	}
}

func TestGetSchemeQuote(t *testing.T) {
	mft := mftool.NewMftool()
	code := "101305"
	if v := mft.GetSchemeQuote(code); reflect.TypeOf(v).Kind() != reflect.Map {
		t.Errorf("Expected dict/map response for valid code")
	}
	if v := mft.GetSchemeQuoteAsJSON(code); reflect.TypeOf(v).Kind() != reflect.String {
		t.Errorf("Expected string response for valid code as json")
	}
	if mft.GetSchemeQuote("wrong code") != nil {
		t.Errorf("Expected nil for wrong code")
	}
	if v := mft.GetSchemeQuote(101305); reflect.TypeOf(v).Kind() != reflect.Map {
		t.Errorf("Expected dict for int code")
	}
	if res := mft.GetSchemeQuote(101305); res == nil {
		t.Errorf("Expected data present for int code")
	}
}

func TestGetSchemeHistoricalNav(t *testing.T) {
	mft := mftool.NewMftool()
	code := "101305"
	if v := mft.GetSchemeHistoricalNav(code); reflect.TypeOf(v).Kind() != reflect.Map {
		t.Errorf("Expected dict/map response for valid code")
	}
	if v := mft.GetSchemeHistoricalNavAsJSON(code); reflect.TypeOf(v).Kind() != reflect.String {
		t.Errorf("Expected string response for valid code as json")
	}
	if mft.GetSchemeHistoricalNav("wrong code") != nil {
		t.Errorf("Expected nil for wrong code")
	}
	if v := mft.GetSchemeHistoricalNav(101305); reflect.TypeOf(v).Kind() != reflect.Map {
		t.Errorf("Expected dict for int code")
	}
	if res := mft.GetSchemeHistoricalNav(101305); res == nil {
		t.Errorf("Expected data present for int code")
	}
}

func TestGetSchemeDetails(t *testing.T) {
	mft := mftool.NewMftool()
	code := "101305"
	if v := mft.GetSchemeDetails(code); reflect.TypeOf(v).Kind() != reflect.Map {
		t.Errorf("Expected dict/map response for valid code")
	}
	if v := mft.GetSchemeDetailsAsJSON(code); reflect.TypeOf(v).Kind() != reflect.String {
		t.Errorf("Expected string response for valid code as json")
	}
	if mft.GetSchemeDetails("wrong code") != nil {
		t.Errorf("Expected nil for wrong code")
	}
	if v := mft.GetSchemeDetails(101305); reflect.TypeOf(v).Kind() != reflect.Map {
		t.Errorf("Expected dict for int code")
	}
	if res := mft.GetSchemeDetails(101305); res == nil {
		t.Errorf("Expected data present for int code")
	}
}

func TestCalculateBalanceUnitsValue(t *testing.T) {
	mft := mftool.NewMftool()
	code := "101305"
	result := mft.CalculateBalanceUnitsValue(code, 221)
	if result == nil {
		t.Errorf("Result of CalculateBalanceUnitsValue is nil")
	}
}

func TestGetSchemeHistoricalNavYear(t *testing.T) {
	mft := mftool.NewMftool()
	code := "101305"
	if v := mft.GetSchemeHistoricalNavYear(code, 2018); reflect.TypeOf(v).Kind() != reflect.Map {
		t.Errorf("Expected dict/map response for valid code and year")
	}
	if v := mft.GetSchemeHistoricalNavYearAsJSON(code, 2018); reflect.TypeOf(v).Kind() != reflect.String {
		t.Errorf("Expected string response for valid code+year as json")
	}
	if mft.GetSchemeHistoricalNavYear("wrong code", 2018) != nil {
		t.Errorf("Expected nil for wrong code")
	}
	if v := mft.GetSchemeHistoricalNavYear(101305, 2018); reflect.TypeOf(v).Kind() != reflect.Map {
		t.Errorf("Expected dict for int code")
	}
	if res := mft.GetSchemeHistoricalNavYear(101305, 2018); res == nil {
		t.Errorf("Expected data present for int code+year")
	}
}

func TestGetDay(t *testing.T) {
	if mftool.IsHoliday() {
		if !mftool.GetFriday() {
			t.Errorf("GetFriday() should return true on holiday")
		}
	} else {
		if !mftool.GetToday() {
			t.Errorf("GetToday() should return true on non-holiday")
		}
	}
}

// Assumes the existence of the following method signatures:
//   func GetSchemeHistoricalNavForDates(code interface{}, from, to string) map[string]interface{}
//   func GetSchemeHistoricalNavForDatesAsJSON(code interface{}, from, to string) string
func TestGetSchemeHistoricalNavForDates(t *testing.T) {
	mft := mftool.NewMftool()
	code := "101305"
	if v := mft.GetSchemeHistoricalNavForDates(code, "1-1-2018", "31-12-2018"); reflect.TypeOf(v).Kind() != reflect.Map {
		t.Errorf("Expected dict/map response for valid code")
	}
	if v := mft.GetSchemeHistoricalNavForDatesAsJSON(code, "1-1-2018", "31-12-2018"); reflect.TypeOf(v).Kind() != reflect.String {
		t.Errorf("Expected string response for valid code as json")
	}
	if mft.GetSchemeHistoricalNavForDates("wrong code", "1-1-2018", "31-12-2018") != nil {
		t.Errorf("Expected nil for wrong code")
	}
	if v := mft.GetSchemeHistoricalNavForDates(101305, "1-1-2018", "31-12-2018"); reflect.TypeOf(v).Kind() != reflect.Map {
		t.Errorf("Expected map for int code")
	}
	if res := mft.GetSchemeHistoricalNavForDates(101305, "1-1-2018", "31-12-2018"); res == nil {
		t.Errorf("Expected data present")
	}
}

func TestGetOpenEndedEquitySchemePerformance(t *testing.T) {
	mft := mftool.NewMftool()
	if v := mft.GetOpenEndedEquitySchemePerformance(false); reflect.TypeOf(v).Kind() != reflect.Map {
		t.Errorf("Expected dict/map result")
	}
	result := mft.GetOpenEndedEquitySchemePerformance(false)
	emptyDict := map[string]interface{}{
		"Large Cap":         []interface{}{},
		"Large & Mid Cap":   []interface{}{},
		"Multi Cap":         []interface{}{},
		"Mid Cap":           []interface{}{},
		"Small Cap":         []interface{}{},
		"Value":             []interface{}{},
		"ELSS":              []interface{}{},
		"Contra":            []interface{}{},
		"Dividend Yield":    []interface{}{},
		"Focused":           []interface{}{},
	}
	if reflect.DeepEqual(result, emptyDict) {
		t.Errorf("Expected non-empty performance result")
	}
}