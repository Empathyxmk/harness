package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type FeatureCollection struct {
	features []*Feature
}

func (fc *FeatureCollection) Add(f *Feature) *FeatureCollection {
	fc.features = append(fc.features, f)
	return fc
}
func (fc *FeatureCollection) SetFeatures(fs []*Feature) {
	fc.features = fs
}
func (fc *FeatureCollection) GetFeatures() []*Feature {
	return fc.features
}
func (fc *FeatureCollection) String() string {
	return "FeatureCollection" // For test
}
func (fc *FeatureCollection) Accept(visitor GeoJsonObjectVisitor[string]) string {
	return visitor.VisitFeatureCollection(fc)
}
func (fc *FeatureCollection) Equal(other *FeatureCollection) bool {
	if len(fc.features) != len(other.features) {
		return false
	}
	for i, f := range fc.features {
		if f != other.features[i] {
			return false
		}
	}
	return true
}
func (fc *FeatureCollection) HashCode() int {
	return len(fc.features)
}

type Feature struct {
	id string
}
func (f *Feature) SetId(id string)      { f.id = id }
func (f *Feature) GetId() string        { return f.id }
func (f *Feature) Equal(other *Feature) bool { return f.id == other.id }
func (f *Feature) String() string       { return "Feature{id='" + f.id + "'}" }

type Point struct{}
type GeoJsonObjectVisitor[T any] interface {
	VisitFeatureCollection(fc *FeatureCollection) T
	VisitPoint(p *Point) T
	VisitMultiPoint(mp *MultiPoint) T
	VisitLineString(ls *LineString) T
	VisitMultiLineString(mls *MultiLineString) T
	VisitPolygon(p *Polygon) T
	VisitMultiPolygon(mp *MultiPolygon) T
	VisitGeometryCollection(gc *GeometryCollection) T
	VisitFeature(f *Feature) T
}
type MultiPoint struct{}
type LineString struct{}
type MultiLineString struct{}
type Polygon struct{}
type MultiPolygon struct{}
type GeometryCollection struct{}

type dummyVisitor struct{}

func (v *dummyVisitor) VisitFeatureCollection(fc *FeatureCollection) string { return "public_fc_visited" }
func (v *dummyVisitor) VisitPoint(p *Point) string                         { return "" }
func (v *dummyVisitor) VisitMultiPoint(mp *MultiPoint) string              { return "" }
func (v *dummyVisitor) VisitLineString(ls *LineString) string              { return "" }
func (v *dummyVisitor) VisitMultiLineString(mls *MultiLineString) string   { return "" }
func (v *dummyVisitor) VisitPolygon(p *Polygon) string                     { return "" }
func (v *dummyVisitor) VisitMultiPolygon(mp *MultiPolygon) string          { return "" }
func (v *dummyVisitor) VisitGeometryCollection(gc *GeometryCollection) string {
	return ""
}
func (v *dummyVisitor) VisitFeature(f *Feature) string { return "" }

func TestAddAndGetFeatures_public(t *testing.T) {
	fc := &FeatureCollection{}
	feature1 := &Feature{}
	feature1.SetId("public_id1")
	feature2 := &Feature{}
	feature2.SetId("public_id2")
	fc.Add(feature1)
	fc.Add(feature2)
	assert.Equal(t, 2, len(fc.GetFeatures()))
	assert.Contains(t, fc.GetFeatures(), feature1)
	assert.Contains(t, fc.GetFeatures(), feature2)
}

func TestSetFeatures_public(t *testing.T) {
	fc := &FeatureCollection{}
	a := &Feature{}
	b := &Feature{}
	fc.SetFeatures([]*Feature{a, b})
	assert.Equal(t, 2, len(fc.GetFeatures()))
	assert.Equal(t, a, fc.GetFeatures()[0])
	assert.Equal(t, b, fc.GetFeatures()[1])
}

func TestRemoveFeatures_public(t *testing.T) {
	fc := &FeatureCollection{}
	f1 := &Feature{}
	f1.SetId("one")
	f2 := &Feature{}
	f2.SetId("two")
	fc.Add(f1)
	fc.Add(f2)
	assert.Equal(t, 2, len(fc.GetFeatures()))
	// Remove f1 manually
	var index int = -1
	for i, f := range fc.GetFeatures() {
		if f == f1 {
			index = i
			break
		}
	}
	if index != -1 {
		fc.features = append(fc.features[:index], fc.features[index+1:]...)
	}
	assert.Equal(t, 1, len(fc.GetFeatures()))
	assert.NotContains(t, fc.GetFeatures(), f1)
	assert.Contains(t, fc.GetFeatures(), f2)
}

func TestAccept_public(t *testing.T) {
	fc := &FeatureCollection{}
	result := fc.Accept(&dummyVisitor{})
	assert.Equal(t, "public_fc_visited", result)
}

func TestToString_public(t *testing.T) {
	fc := &FeatureCollection{}
	str := fc.String()
	assert.Contains(t, str, "FeatureCollection")
}

func TestEqualsAndHashCode_public(t *testing.T) {
	fc1 := &FeatureCollection{}
	fc2 := &FeatureCollection{}
	f1 := &Feature{}
	f1.SetId("uniqX")
	f2 := &Feature{}
	f2.SetId("uniqY")
	fc1.Add(f1)
	fc1.Add(f2)
	fc2.SetFeatures([]*Feature{f1, f2})
	assert.True(t, fc1.Equal(fc2))
	assert.Equal(t, fc1.HashCode(), fc2.HashCode())
	assert.False(t, fc1.Equal(nil))
	other := &FeatureCollection{}
	other.Add(&Feature{id: "different_id_for_public"})
	assert.False(t, fc1.Equal(other))
}

func TestGetFeaturesNeverNull_public(t *testing.T) {
	fc := &FeatureCollection{}
	assert.NotNil(t, fc.GetFeatures())
	assert.Equal(t, 0, len(fc.GetFeatures()))
}