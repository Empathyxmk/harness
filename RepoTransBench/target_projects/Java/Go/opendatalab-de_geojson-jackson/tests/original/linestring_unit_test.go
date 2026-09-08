package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type LngLatAlt struct {
	Lon float64
	Lat float64
}

type LineString struct {
	Coords []LngLatAlt
}

func NewLineString(p ...LngLatAlt) *LineString {
	return &LineString{Coords: append([]LngLatAlt{}, p...)}
}
func (ls *LineString) Add(p LngLatAlt) *LineString {
	ls.Coords = append(ls.Coords, p)
	return ls
}
func (ls *LineString) GetCoordinates() []LngLatAlt {
	return ls.Coords
}
func (ls *LineString) String() string {
	return "LineString{coordinates}"
}

type GeoJsonObjectVisitorString interface {
	VisitLineString(*LineString) string
	VisitFeatureCollection(*FeatureCollection) string
	VisitFeature(*Feature) string
	VisitPoint(*Point) string
	VisitMultiPoint(*MultiPoint) string
	VisitMultiLineString(*MultiLineString) string
	VisitPolygon(*Polygon) string
	VisitMultiPolygon(*MultiPolygon) string
	VisitGeometryCollection(*GeometryCollection) string
}
type FeatureCollection struct{}
type Feature struct{}
type Point struct{}
type MultiPoint struct{}
type MultiLineString struct{}
type Polygon struct{}
type MultiPolygon struct{}
type GeometryCollection struct{}

type visitorLS struct{}

func (v *visitorLS) VisitLineString(ls *LineString) string { return "ok" }
func (v *visitorLS) VisitFeatureCollection(_ *FeatureCollection) string {
	return ""
}
func (v *visitorLS) VisitFeature(_ *Feature) string              { return "" }
func (v *visitorLS) VisitPoint(_ *Point) string                  { return "" }
func (v *visitorLS) VisitMultiPoint(_ *MultiPoint) string        { return "" }
func (v *visitorLS) VisitMultiLineString(_ *MultiLineString) string {
	return ""
}
func (v *visitorLS) VisitPolygon(_ *Polygon) string            { return "" }
func (v *visitorLS) VisitMultiPolygon(_ *MultiPolygon) string  { return "" }
func (v *visitorLS) VisitGeometryCollection(_ *GeometryCollection) string {
	return ""
}

func (ls *LineString) Accept(visitor GeoJsonObjectVisitorString) string {
	return visitor.VisitLineString(ls)
}

func (ls *LineString) Equal(other *LineString) bool {
	if other == nil || len(ls.Coords) != len(other.Coords) {
		return false
	}
	for i, coord := range ls.Coords {
		if coord != other.Coords[i] {
			return false
		}
	}
	return true
}

func (ls *LineString) HashCode() int {
	return len(ls.Coords)
}

func TestLineString_ConstructorAndAdd(t *testing.T) {
	p1 := LngLatAlt{1, 2}
	p2 := LngLatAlt{2, 3}
	line := NewLineString(p1)
	line.Add(p2)
	assert.Equal(t, 2, len(line.GetCoordinates()))
	assert.Equal(t, p1, line.GetCoordinates()[0])
	assert.Equal(t, p2, line.GetCoordinates()[1])
}

func TestLineString_Accept(t *testing.T) {
	line := NewLineString()
	result := line.Accept(&visitorLS{})
	assert.Equal(t, "ok", result)
}

func TestLineString_EqualsAndHashCode(t *testing.T) {
	l1 := NewLineString(LngLatAlt{1, 2})
	l2 := NewLineString(LngLatAlt{1, 2})
	assert.True(t, l1.Equal(l2))
	assert.Equal(t, l1.HashCode(), l2.HashCode())
	assert.False(t, l1.Equal(nil))
	assert.False(t, l1.Equal(NewLineString()))
	l3 := NewLineString(LngLatAlt{2, 2})
	assert.False(t, l1.Equal(l3))
}

func TestLineString_ToString(t *testing.T) {
	l := NewLineString()
	assert.Contains(t, l.String(), "coordinates")
}