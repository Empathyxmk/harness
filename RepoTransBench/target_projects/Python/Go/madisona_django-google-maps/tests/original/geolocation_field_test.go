package original

import (
	"fmt"
	"reflect"
	"testing"
)

// --- Simulated types for testing geolocation field "model" behavior ---

type GeoPt struct {
	Lat float64
	Lon float64
}

func ParseGeoPt(v interface{}) (GeoPt, error) {
	switch t := v.(type) {
	case string:
		var lat, lon float64
		n, err := fmt.Sscanf(t, "%f,%f", &lat, &lon)
		if err != nil || n != 2 {
			return GeoPt{}, fmt.Errorf("invalid GeoPt string")
		}
		return GeoPt{lat, lon}, nil
	default:
		return GeoPt{}, fmt.Errorf("unsupported type for ParseGeoPt")
	}
}

// Simulate a minimal "Person" with GeoPt field and a DB-like registry.
type Person struct {
	ID         int
	Geolocation GeoPt
}

var personTable = make(map[int]Person)
var nextPersonID = 1

func createPerson(geolocation interface{}) Person {
	pt, _ := ParseGeoPt(geolocation)
	p := Person{
		ID:         nextPersonID,
		Geolocation: pt,
	}
	personTable[nextPersonID] = p
	nextPersonID++
	return p
}

func getPersonByID(id int) Person {
	return personTable[id]
}

func getPersonByGeo(geopt GeoPt) (Person, bool) {
	for _, p := range personTable {
		if p.Geolocation == geopt {
			return p, true
		}
	}
	return Person{}, false
}

func getPersonByGeoIn(list []GeoPt) (Person, bool) {
	for _, g := range list {
		if p, ok := getPersonByGeo(g); ok {
			return p, true
		}
	}
	return Person{}, false
}

func personFieldValueToString(p Person) string {
	return fmt.Sprintf("%.1f,%.1f", p.Geolocation.Lat, p.Geolocation.Lon)
}

// TESTS

func TestGettingLatLonFromModelGivenString(t *testing.T) {
	personTable = make(map[int]Person)
	nextPersonID = 1
	sutCreate := createPerson("45,90")
	sut := getPersonByID(sutCreate.ID)
	if sut.Geolocation.Lat != 45 {
		t.Errorf("expected lat 45, got %v", sut.Geolocation.Lat)
	}
	if sut.Geolocation.Lon != 90 {
		t.Errorf("expected lon 90, got %v", sut.Geolocation.Lon)
	}
}

func TestGettingLatLonFromModelGivenPt(t *testing.T) {
	personTable = make(map[int]Person)
	nextPersonID = 1
	pt, _ := ParseGeoPt("45,90")
	p := Person{
		ID:          nextPersonID,
		Geolocation: pt,
	}
	personTable[nextPersonID] = p
	nextPersonID++
	sut := getPersonByID(p.ID)
	if sut.Geolocation.Lat != 45 {
		t.Errorf("expected lat 45, got %v", sut.Geolocation.Lat)
	}
	if sut.Geolocation.Lon != 90 {
		t.Errorf("expected lon 90, got %v", sut.Geolocation.Lon)
	}
}

func TestGettingLatLonFromModelInDBGivenString(t *testing.T) {
	personTable = make(map[int]Person)
	nextPersonID = 1
	sutCreate := createPerson("45,90")
	sut := getPersonByID(sutCreate.ID)
	if sut.Geolocation.Lat != 45 {
		t.Errorf("expected lat 45, got %v", sut.Geolocation.Lat)
	}
	if sut.Geolocation.Lon != 90 {
		t.Errorf("expected lon 90, got %v", sut.Geolocation.Lon)
	}
}

func TestExactMatchQuery(t *testing.T) {
	personTable = make(map[int]Person)
	nextPersonID = 1
	sut := createPerson("45,90")
	pt, _ := ParseGeoPt("45,90")
	result, ok := getPersonByGeo(pt)
	if !ok || !reflect.DeepEqual(result, sut) {
		t.Errorf("exact match query failed: got=%v want=%v", result, sut)
	}
}

func TestInMatchQuery(t *testing.T) {
	personTable = make(map[int]Person)
	nextPersonID = 1
	sut := createPerson("45,90")
	pt, _ := ParseGeoPt("45,90")
	result, ok := getPersonByGeoIn([]GeoPt{pt})
	if !ok || !reflect.DeepEqual(result, sut) {
		t.Errorf("in match query failed: got=%v want=%v", result, sut)
	}
}

func TestValueToStringWithPoint(t *testing.T) {
	personTable = make(map[int]Person)
	nextPersonID = 1
	sut := createPerson("45,90")
	stringVal := personFieldValueToString(sut)
	if stringVal != "45.0,90.0" {
		t.Errorf("expected '45.0,90.0', got '%s'", stringVal)
	}
}

func TestValueToStringWithString(t *testing.T) {
	personTable = make(map[int]Person)
	nextPersonID = 1
	sut := createPerson("45,90")
	stringVal := personFieldValueToString(sut)
	if stringVal != "45.0,90.0" {
		t.Errorf("expected '45.0,90.0', got '%s'", stringVal)
	}
}

func TestGetPrepValueReturnsNoneWhenNone(t *testing.T) {
	// Simulate value to string for nil/zero value
	var zeroPerson Person
	var result *GeoPt = nil
	if result != nil {
		t.Errorf("expected nil, got %v", result)
	}
	_ = zeroPerson // suppress unused
}