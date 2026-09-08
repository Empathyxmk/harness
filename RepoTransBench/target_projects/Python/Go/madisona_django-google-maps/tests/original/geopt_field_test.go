package original

import (
	"errors"
	"fmt"
	"testing"
)

type GeoPt struct {
	Lat *float64
	Lon *float64
}

func NewGeoPt(s string) (GeoPt, error) {
	if s == "" {
		return GeoPt{nil, nil}, nil
	}
	var lat, lon float64
	n, err := fmt.Sscanf(s, "%f,%f", &lat, &lon)
	if err != nil || n != 2 {
		return GeoPt{}, errors.New("invalid GeoPt")
	}
	if lat > 90.0 || lat < -90.0 || lon > 180.0 || lon < -180.0 {
		return GeoPt{}, errors.New("lat/lon out of range")
	}
	return GeoPt{&lat, &lon}, nil
}

func (g GeoPt) String() string {
	if g.Lat == nil || g.Lon == nil {
		return ""
	}
	return fmt.Sprintf("%g,%g", *g.Lat, *g.Lon)
}

func (g GeoPt) Equal(other interface{}) bool {
	o, ok := other.(GeoPt)
	if !ok {
		return false
	}
	if g.Lat == nil || g.Lon == nil || o.Lat == nil || o.Lon == nil {
		return g.Lat == o.Lat && g.Lon == o.Lon
	}
	return *g.Lat == *o.Lat && *g.Lon == *o.Lon
}

func TestSetsLatLonOnInitialization(t *testing.T) {
	geoPt, err := NewGeoPt("15.001,32.001")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if *geoPt.Lat != 15.001 {
		t.Errorf("expected 15.001, got %v", geoPt.Lat)
	}
	if *geoPt.Lon != 32.001 {
		t.Errorf("expected 32.001, got %v", geoPt.Lon)
	}
}

func TestUsesLatCommaLonAsString(t *testing.T) {
	geoPt, _ := NewGeoPt("15.001,32.001")
	if geoPt.String() != "15.001,32.001" {
		t.Errorf("expected '15.001,32.001', got %s", geoPt.String())
	}
}

func TestTwoGeoPtsWithSameLatLonShouldBeEqual(t *testing.T) {
	geoPt1, _ := NewGeoPt("15.001,32.001")
	geoPt2, _ := NewGeoPt("15.001,32.001")
	if !geoPt1.Equal(geoPt2) {
		t.Errorf("GeoPts should be equal")
	}
}

func TestTwoGeoPtsWithDifferentLatShouldNotBeEqual(t *testing.T) {
	geoPt1, _ := NewGeoPt("15.001,32.001")
	geoPt2, _ := NewGeoPt("20.001,32.001")
	if geoPt1.Equal(geoPt2) {
		t.Errorf("GeoPts with different lat should not be equal")
	}
}

func TestTwoGeoPtsWithDifferentLonShouldNotBeEqual(t *testing.T) {
	geoPt1, _ := NewGeoPt("15.001,32.001")
	geoPt2, _ := NewGeoPt("15.001,62.001")
	if geoPt1.Equal(geoPt2) {
		t.Errorf("GeoPts with different lon should not be equal")
	}
}

func TestIsNotEqualWhenComparisonIsNotGeoPtObject(t *testing.T) {
	geoPt1, _ := NewGeoPt("15.001,32.001")
	var other interface{} = "15.001,32.001"
	if geoPt1.Equal(other) {
		t.Errorf("GeoPt should not equal string value")
	}
}

func TestAllowsGeoPtInstantiatedWithEmptyString(t *testing.T) {
	geoPt, _ := NewGeoPt("")
	if geoPt.Lat != nil || geoPt.Lon != nil {
		t.Errorf("expected nil lat/lon for empty string")
	}
}

func TestUsesEmptyStringAsStringForEmptyGeoPt(t *testing.T) {
	geoPt, _ := NewGeoPt("")
	if geoPt.String() != "" {
		t.Errorf("expected empty string, got '%s'", geoPt.String())
	}
}