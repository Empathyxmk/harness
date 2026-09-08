package public_tests

import (
	"math/rand"
	"testing"
	"github.com/stretchr/testify/assert"
	"agarciadom_xeger/xeger"
)

func TestXegerCoveragePublic_ConstructorWithRandom(t *testing.T) {
	x := xeger.NewXegerWithRand("xyz|uvw", rand.New(rand.NewSource(321)))
	assert.NotNil(t, x)
	assert.NotNil(t, x.GetRandom())
}

func TestXegerCoveragePublic_SetAndGetRandom(t *testing.T) {
	x := xeger.NewXegerWithRand("b+", rand.New(rand.NewSource(4545)))
	r := rand.New(rand.NewSource(999))
	x.SetRandom(r)
	assert.Equal(t, r, x.GetRandom())
}

func TestXegerCoveragePublic_GenerateSimpleLiteral(t *testing.T) {
	x := xeger.NewXegerWithRand("acd", rand.New(rand.NewSource(222)))
	assert.Equal(t, "acd", x.Generate())
}

func TestXegerCoveragePublic_GenerateWithDefaultRandom(t *testing.T) {
	x := xeger.NewXeger("z")
	assert.Equal(t, "z", x.Generate())
}

func TestXegerCoveragePublic_GetRandomIntWorksOnSimpleCases(t *testing.T) {
	r1 := xeger.GetRandomInt(8, 8, rand.New(rand.NewSource(5)))
	assert.Equal(t, 8, r1)
	r2 := xeger.GetRandomInt(2, 8, rand.New(rand.NewSource(7)))
	assert.True(t, r2 >= 2 && r2 <= 8)
}

func TestXegerCoveragePublic_GenerateWithBoundedLengthThrowsMinimum(t *testing.T) {
	x := xeger.NewXegerWithRand("b?", rand.New(rand.NewSource(4)))
	_, err := x.GenerateWithBounds(2, 2)
	if err == nil {
		t.Fatalf("Should have thrown FailedRandomWalkError")
	}
	if msg := err.Error(); !(msg == "current = 0 < min = 2" || msg == "current = 1 < min = 2") {
		t.Errorf("Unexpected error message: %s", msg)
	}
}

func TestXegerCoveragePublic_GenerateWithBoundedLengthThrowsMaximum(t *testing.T) {
	x := xeger.NewXegerWithRand("b{5}", rand.New(rand.NewSource(4)))
	_, err := x.GenerateWithBounds(1, 3)
	if err == nil {
		t.Fatalf("Should have thrown FailedRandomWalkError")
	}
	if msg := err.Error(); !assert.Contains(t, msg, "exceeded maximum walk length") {
		t.Errorf("Unexpected error: %s", msg)
	}
}

func TestXegerCoveragePublic_GenerateWithBoundedLengthProducesAcceptableLength(t *testing.T) {
	x := xeger.NewXegerWithRand("c{1,3}", rand.New(rand.NewSource(5)))
	val, err := x.GenerateWithBounds(1, 3)
	assert.Nil(t, err)
	assert.True(t, len(val) >= 1 && len(val) <= 3)
}

func TestXegerCoveragePublic_FailedRandomWalkError(t *testing.T) {
	e := xeger.FailedRandomWalkError{"another fail"}
	assert.NotNil(t, e.Error())
	assert.Equal(t, "another fail", e.Error())
}