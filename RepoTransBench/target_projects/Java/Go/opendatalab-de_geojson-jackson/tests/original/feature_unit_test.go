package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type FeatureProperties struct {
	props map[string]interface{}
}

type Feature struct {
	geometry any
	id       string
	props    map[string]interface{}
}

func (f *Feature) SetProperty(key string, val interface{}) {
	if f.props == nil {
		f.props = map[string]interface{}{}
	}
	f.props[key] = val
}
func (f *Feature) GetProperty(key string) interface{} {
	if f.props == nil {
		return nil
	}
	return f.props[key]
}
func (f *Feature) SetProperties(mp map[string]interface{}) {
	f.props = mp
}
func (f *Feature) GetProperties() map[string]interface{} {
	return f.props
}

func (f *Feature) SetGeometry(g any) {
	f.geometry = g
}
func (f *Feature) GetGeometry() any {
	return f.geometry
}
func (f *Feature) SetId(id string) {
	f.id = id
}
func (f *Feature) GetId() string {
	return f.id
}

type Point struct{}

type GeoJsonObjectVisitorString interface {
	VisitFeature(*Feature) string
	VisitFeatureCollection(*FeatureCollection) string
	VisitPoint(*Point) string
	VisitMultiPoint(*MultiPoint) string
	VisitLineString(*LineString) string
	VisitMultiLineString(*MultiLineString) string
	VisitPolygon(*Polygon) string
	VisitMultiPolygon(*MultiPolygon) string
	VisitGeometryCollection(*GeometryCollection) string
}
type FeatureCollection struct{}
type MultiPoint struct{}
type LineString struct{}
type MultiLineString struct{}
type Polygon struct{}
type MultiPolygon struct{}
type GeometryCollection struct{}

type featureUnitVisitor struct{}

func (v *featureUnitVisitor) VisitFeature(f *Feature) string               { return "visited" }
func (v *featureUnitVisitor) VisitFeatureCollection(*FeatureCollection) string { return "" }
func (v *featureUnitVisitor) VisitPoint(*Point) string                     { return "" }
func (v *featureUnitVisitor) VisitMultiPoint(*MultiPoint) string           { return "" }
func (v *featureUnitVisitor) VisitLineString(*LineString) string           { return "" }
func (v *featureUnitVisitor) VisitMultiLineString(*MultiLineString) string { return "" }
func (v *featureUnitVisitor) VisitPolygon(*Polygon) string                 { return "" }
func (v *featureUnitVisitor) VisitMultiPolygon(*MultiPolygon) string       { return "" }
func (v *featureUnitVisitor) VisitGeometryCollection(*GeometryCollection) string { return "" }

func (f *Feature) Accept(visitor GeoJsonObjectVisitorString) string {
	return visitor.VisitFeature(f)
}

func (f1 *Feature) Equal(f2 *Feature) bool {
	if f2 == nil {
		return false
	}
	if f1.id != f2.id {
		return false
	}
	if !assert.ObjectsAreEqual(f1.props, f2.props) {
		return false
	}
	if !assert.ObjectsAreEqual(f1.geometry, f2.geometry) {
		return false
	}
	return true
}

func (f *Feature) HashCode() int {
	hash := 0
	for k := range f.props {
		hash += len(k)
	}
	if f.id != "" {
		hash += len(f.id)
	}
	return hash
}

func (f *Feature) String() string {
	return "Feature{id='" + f.id + "'}"
}

func TestFeatureUnitTest_PropertiesSetGet(t *testing.T) {
	feature := &Feature{}
	feature.SetProperty("key", "val")
	assert.Equal(t, "val", feature.GetProperty("key"))
	mp := map[string]interface{}{"a": 1}
	feature.SetProperties(mp)
	assert.Equal(t, mp, feature.GetProperties())
}

func TestFeatureUnitTest_GeometrySetGet(t *testing.T) {
	feature := &Feature{}
	p := &Point{}
	feature.SetGeometry(p)
	assert.Equal(t, p, feature.GetGeometry())
}

func TestFeatureUnitTest_IdSetGet(t *testing.T) {
	feature := &Feature{}
	feature.SetId("x")
	assert.Equal(t, "x", feature.GetId())
}

func TestFeatureUnitTest_Accept(t *testing.T) {
	feature := &Feature{}
	result := feature.Accept(&featureUnitVisitor{})
	assert.Equal(t, "visited", result)
}

func TestFeatureUnitTest_EqualsAndHashCode(t *testing.T) {
	f1 := &Feature{}
	f2 := &Feature{}
	f1.SetId("1")
	f2.SetId("1")
	f1.SetProperty("x", "y")
	f2.SetProperty("x", "y")
	f1.SetGeometry(&Point{})
	f2.SetGeometry(&Point{})
	assert.True(t, f1.Equal(f2))
	assert.Equal(t, f1.HashCode(), f2.HashCode())
	assert.False(t, f1.Equal(nil))
	assert.False(t, f1.Equal(&Feature{props: map[string]interface{}{"z": 1}}))
	f2.SetId("2")
	assert.False(t, f1.Equal(f2))
}

func TestFeatureUnitTest_ToString(t *testing.T) {
	feature := &Feature{}
	assert.Contains(t, feature.String(), "Feature{")
}