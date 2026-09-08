package original

import (
	"math/rand"
	"testing"
	"github.com/stretchr/testify/assert"
	"agarciadom_xeger/xeger"
)

func TestXegerCoverage_ConstructorWithRandom(t *testing.T) {
	x := xeger.NewXegerWithRand("abc|def", rand.New(rand.NewSource(123)))
	assert.NotNil(t, x)
	assert.NotNil(t, x.GetRandom())
}

func TestXegerCoverage_SetAndGetRandom(t *testing.T) {
	x := xeger.NewXegerWithRand("a+", rand.New(rand.NewSource(123)))
	r := rand.New(rand.NewSource(456))
	x.SetRandom(r)
	assert.Equal(t, r, x.GetRandom())
}

func TestXegerCoverage_GenerateSimpleLiteral(t *testing.T) {
	x := xeger.NewXegerWithRand("abc", rand.New(rand.NewSource(321)))
	g := x.Generate()
	assert.Equal(t, "abc", g)
}

func TestXegerCoverage_GenerateWithDefaultRandom(t *testing.T) {
	x := xeger.NewXeger("b")
	g := x.Generate()
	assert.Equal(t, "b", g)
}

func TestXegerCoverage_GetRandomIntWorksOnSimpleCases(t *testing.T) {
	r1 := xeger.GetRandomInt(5, 5, rand.New(rand.NewSource(1)))
	assert.Equal(t, 5, r1)
	r2 := xeger.GetRandomInt(1, 10, rand.New(rand.NewSource(1)))
	assert.True(t, r2 >= 1 && r2 <= 10)
}

func TestXegerCoverage_GenerateWithBoundedLengthThrowsMinimum(t *testing.T) {
	x := xeger.NewXegerWithRand("a?", rand.New(rand.NewSource(1)))
	_, err := x.GenerateWithBounds(2, 2)
	if err == nil {
		t.Fatalf("Should have thrown FailedRandomWalkError")
	}
	if msg := err.Error(); !(msg == "current = 0 < min = 2" || msg == "current = 1 < min = 2") {
		t.Errorf("Unexpected error message: %s", msg)
	}
}

func TestXegerCoverage_GenerateWithBoundedLengthThrowsMaximum(t *testing.T) {
	x := xeger.NewXegerWithRand("a{3}", rand.New(rand.NewSource(1)))
	_, err := x.GenerateWithBounds(1, 2)
	if err == nil {
		t.Fatalf("Should have thrown FailedRandomWalkError")
	}
	if msg := err.Error(); !assert.Contains(t, msg, "exceeded maximum walk length") {
		t.Errorf("Unexpected error: %s", msg)
	}
}

func TestXegerCoverage_GenerateWithBoundedLengthProducesAcceptableLength(t *testing.T) {
	x := xeger.NewXegerWithRand("a{2,4}", rand.New(rand.NewSource(2)))
	val, err := x.GenerateWithBounds(2, 4)
	assert.Nil(t, err)
	assert.True(t, len(val) >= 2 && len(val) <= 4)
	// TODO: regex match
}

func TestXegerCoverage_FailedRandomWalkError(t *testing.T) {
	e := xeger.FailedRandomWalkError{"fail"}
	assert.NotNil(t, e.Error())
	assert.Equal(t, "fail", e.Error())
}