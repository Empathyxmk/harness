package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"reflect"
)

type FeatureCollection struct {
	features []*Feature
}

func (fc *FeatureCollection) Add(f *Feature) *FeatureCollection {
	fc.features = append(fc.features, f)
	return fc
}

func (fc *FeatureCollection) AddAll(fs []*Feature) *FeatureCollection {
	fc.features = append(fc.features, fs...)
	return fc
}

func (fc *FeatureCollection) GetFeatures() []*Feature {
	return fc.features
}

func (fc *FeatureCollection) SetFeatures(fs []*Feature) {
	fc.features = fs
}

func (fc *FeatureCollection) Iterator() <-chan *Feature {
	ch := make(chan *Feature)
	go func() {
		for _, f := range fc.features {
			ch <- f
		}
		close(ch)
	}()
	return ch
}

// Dummy Visitor pattern for demonstration
type GeoJsonObjectVisitor[T any] interface {
	VisitFeatureCollection(*FeatureCollection) T
	VisitFeature(*Feature) T
	VisitPoint(*Point) T
	VisitMultiPoint(*MultiPoint) T
	VisitLineString(*LineString) T
	VisitMultiLineString(*MultiLineString) T
	VisitPolygon(*Polygon) T
	VisitMultiPolygon(*MultiPolygon) T
	VisitGeometryCollection(*GeometryCollection) T
}

func (fc *FeatureCollection) Accept(visitor GeoJsonObjectVisitor[string]) string {
	return visitor.VisitFeatureCollection(fc)
}

func (fc *FeatureCollection) Equal(other *FeatureCollection) bool {
	if other == nil {
		return false
	}
	return reflect.DeepEqual(fc.features, other.features)
}

func (fc *FeatureCollection) HashCode() int {
	return len(fc.features)
}

func (fc *FeatureCollection) String() string {
	return "FeatureCollection{features...}" // Simplified for demo
}

// Dummy structs for compatibility
type Feature struct{ id string }
type Point struct{}
type MultiPoint struct{}
type LineString struct{}
type MultiLineString struct{}
type Polygon struct{}
type MultiPolygon struct{}
type GeometryCollection struct{}

func TestFeatureCollection_AddAndGetFeatures(t *testing.T) {
	fc := &FeatureCollection{}
	f1 := &Feature{}
	f2 := &Feature{}
	fc.Add(f1).Add(f2)
	features := fc.GetFeatures()
	assert.Equal(t, 2, len(features))
	assert.Contains(t, features, f1)
	assert.Contains(t, features, f2)
}

func TestFeatureCollection_SetFeatures(t *testing.T) {
	fc := &FeatureCollection{}
	f := &Feature{}
	fc.SetFeatures([]*Feature{f})
	assert.Equal(t, []*Feature{f}, fc.GetFeatures())
}

func TestFeatureCollection_AddAll(t *testing.T) {
	fc := &FeatureCollection{}
	f1 := &Feature{}
	f2 := &Feature{}
	fc.AddAll([]*Feature{f1, f2})
	assert.Contains(t, fc.GetFeatures(), f1)
	assert.Contains(t, fc.GetFeatures(), f2)
}

func TestFeatureCollection_Iterator(t *testing.T) {
	fc := &FeatureCollection{}
	f1 := &Feature{}
	fc.Add(f1)
	found := false
	for f := range fc.Iterator() {
		if f == f1 {
			found = true
			break
		}
	}
	assert.True(t, found)
}

type testVisitor struct{}

func (v *testVisitor) VisitFeatureCollection(fc *FeatureCollection) string { return "visited" }
func (v *testVisitor) VisitFeature(f *Feature) string                     { return "" }
func (v *testVisitor) VisitPoint(p *Point) string                         { return "" }
func (v *testVisitor) VisitMultiPoint(mp *MultiPoint) string              { return "" }
func (v *testVisitor) VisitLineString(ls *LineString) string              { return "" }
func (v *testVisitor) VisitMultiLineString(mls *MultiLineString) string   { return "" }
func (v *testVisitor) VisitPolygon(p *Polygon) string                     { return "" }
func (v *testVisitor) VisitMultiPolygon(mp *MultiPolygon) string          { return "" }
func (v *testVisitor) VisitGeometryCollection(gc *GeometryCollection) string {
	return ""
}

func TestFeatureCollection_Accept(t *testing.T) {
	fc := &FeatureCollection{}
	result := fc.Accept(&testVisitor{})
	assert.Equal(t, "visited", result)
}

func TestFeatureCollection_EqualsAndHashCode(t *testing.T) {
	fc1 := &FeatureCollection{}
	fc2 := &FeatureCollection{}
	f := &Feature{}
	fc1.Add(f)
	fc2.Add(f)
	assert.True(t, fc1.Equal(fc2))
	assert.Equal(t, fc1.HashCode(), fc2.HashCode())
	assert.False(t, fc1.Equal(nil))
	other := &Feature{}
	assert.False(t, fc1.Equal(&FeatureCollection{features: []*Feature{other}}))
	assert.False(t, fc1.Equal(&FeatureCollection{}))
}

func TestFeatureCollection_ToString(t *testing.T) {
	fc := &FeatureCollection{}
	assert.Contains(t, fc.String(), "features")
}