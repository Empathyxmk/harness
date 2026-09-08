package original

import (
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
)

type DummyGeometry struct {
	Coordinates []string
}

func (g *DummyGeometry) Add(val string) *DummyGeometry {
	g.Coordinates = append(g.Coordinates, val)
	return g
}
func (g *DummyGeometry) GetCoordinates() []string {
	return g.Coordinates
}
func (g *DummyGeometry) SetCoordinates(coords []string) {
	g.Coordinates = coords
}

func NewDummyGeometry(vals ...string) *DummyGeometry {
	g := &DummyGeometry{}
	g.SetCoordinates(vals)
	return g
}

func (g *DummyGeometry) Accept(_ interface{}) interface{} { return nil }

func (g *DummyGeometry) Equal(other *DummyGeometry) bool {
	return reflect.DeepEqual(g.Coordinates, other.Coordinates)
}
func (g *DummyGeometry) HashCode() int { return len(g.Coordinates) }
func (g *DummyGeometry) String() string { return "DummyGeometry{coordinates}" }

type Feature struct{}

func TestGeometry_AddAndGetCoordinates(t *testing.T) {
	g := &DummyGeometry{}
	g.Add("A").Add("B")
	coords := g.GetCoordinates()
	assert.Equal(t, 2, len(coords))
	assert.Equal(t, "A", coords[0])
}

func TestGeometry_SetCoordinates(t *testing.T) {
	g := &DummyGeometry{}
	c := []string{"x", "y"}
	g.SetCoordinates(c)
	assert.Equal(t, c, g.GetCoordinates())
}

func TestGeometry_ConstructorWithElements(t *testing.T) {
	g := NewDummyGeometry("p", "q")
	assert.ElementsMatch(t, []string{"p", "q"}, g.GetCoordinates())
}

func TestGeometry_EqualsAndHashCode(t *testing.T) {
	g1 := NewDummyGeometry("a")
	g2 := NewDummyGeometry("a")
	assert.True(t, g1.Equal(g2))
	assert.Equal(t, g1.HashCode(), g2.HashCode())
	assert.False(t, g1.Equal(nil))
	assert.False(t, g1.Equal(&DummyGeometry{Coordinates: []string{"z"}}))
	g3 := NewDummyGeometry("b")
	assert.False(t, g1.Equal(g3))
}

func TestGeometry_ToString(t *testing.T) {
	g := NewDummyGeometry("a")
	assert.Contains(t, g.String(), "coordinates")
}