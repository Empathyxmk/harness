package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type MultiLineString struct {
	Lines [][]LngLatAlt
}

func NewMultiLineString() *MultiLineString {
	return &MultiLineString{Lines: make([][]LngLatAlt, 0)}
}

func (mls *MultiLineString) Add(ls []LngLatAlt) *MultiLineString {
	mls.Lines = append(mls.Lines, ls)
	return mls
}

func (mls *MultiLineString) GetCoordinates() [][]LngLatAlt {
	return mls.Lines
}

func (mls *MultiLineString) Accept(visitor GeoJsonObjectVisitorString) string {
	return visitor.VisitMultiLineString(mls)
}

type GeoJsonObjectVisitorString interface {
	VisitMultiLineString(*MultiLineString) string
	VisitFeatureCollection(*FeatureCollection) string
	VisitFeature(*Feature) string
	VisitPoint(*Point) string
	VisitMultiPoint(*MultiPoint) string
	VisitLineString(*LineString) string
	VisitPolygon(*Polygon) string
	VisitMultiPolygon(*MultiPolygon) string
	VisitGeometryCollection(*GeometryCollection) string
}
type LngLatAlt struct{ Lon, Lat float64 }
type FeatureCollection struct{}
type Feature struct{}
type Point struct{}
type MultiPoint struct{}
type LineString struct{}
type Polygon struct{}
type MultiPolygon struct{}
type GeometryCollection struct{}

type mlsVisitor struct{}

func (v *mlsVisitor) VisitMultiLineString(m *MultiLineString) string       { return "yes" }
func (v *mlsVisitor) VisitFeatureCollection(*FeatureCollection) string     { return "" }
func (v *mlsVisitor) VisitFeature(*Feature) string                        { return "" }
func (v *mlsVisitor) VisitPoint(*Point) string                            { return "" }
func (v *mlsVisitor) VisitMultiPoint(*MultiPoint) string                  { return "" }
func (v *mlsVisitor) VisitLineString(*LineString) string                  { return "" }
func (v *mlsVisitor) VisitPolygon(*Polygon) string                        { return "" }
func (v *mlsVisitor) VisitMultiPolygon(*MultiPolygon) string              { return "" }
func (v *mlsVisitor) VisitGeometryCollection(*GeometryCollection) string  { return "" }

func TestMultiLineString_ConstructorAndAdd(t *testing.T) {
	p1 := LngLatAlt{1, 2}
	p2 := LngLatAlt{3, 4}
	l1 := &LineString{Coords: []LngLatAlt{p1}}
	l2 := &LineString{Coords: []LngLatAlt{p2}}
	mls := NewMultiLineString()
	mls.Add(l1.Coords)
	mls.Add(l2.Coords)
	assert.Equal(t, 2, len(mls.GetCoordinates()))
	assert.Equal(t, l1.Coords, mls.GetCoordinates()[0])
	assert.Equal(t, l2.Coords, mls.GetCoordinates()[1])
}

func TestMultiLineString_Accept(t *testing.T) {
	mls := NewMultiLineString()
	result := mls.Accept(&mlsVisitor{})
	assert.Equal(t, "yes", result)
}