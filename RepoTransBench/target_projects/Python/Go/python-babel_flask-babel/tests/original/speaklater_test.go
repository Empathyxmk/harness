package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type TestFunc func(x interface{}, y ...int) string

func basicFunc(x interface{}, y ...int) string {
	yv := 2
	if len(y) > 0 {
		yv = y[0]
	}
	return "value(" + toString(x) + "," + toString(yv) + ")"
}

func TestStrAndRepr(t *testing.T) {
	lz := NewLazyStringWithFunc(func() string { return basicFunc(1, 3) })
	assert.Equal(t, "value(1,3)", lz.String())
}

func TestLenGetitemIterContains(t *testing.T) {
	lz := NewLazyStringWithFunc(func() string { return "hello world" })
	assert.Equal(t, 11, lz.Len())
	assert.Equal(t, "h", lz.Get(0))
	assert.Equal(t, "ello", lz.Slice(1, 5))
	assert.Equal(t, "hello world", lz.Join())
	assert.True(t, lz.Contains("hello"))
	assert.False(t, lz.Contains("xxx"))
}

func TestAddRadd(t *testing.T) {
	lz := NewLazyStringWithFunc(func() string { return "foo" })
	assert.Equal(t, "foobar", lz.Add("bar"))
	assert.Equal(t, "barfoo", lz.RAdd("bar"))
}

func TestMulRmul(t *testing.T) {
	lz := NewLazyStringWithFunc(func() string { return "a" })
	assert.Equal(t, "aaa", lz.Mul(3))
	assert.Equal(t, "aaa", lz.RMul(3))
}

func TestComparisons(t *testing.T) {
	lz := NewLazyStringWithFunc(func() string { return "b" })
	assert.True(t, lz.Gt("a"))
	assert.True(t, lz.Gte("b"))
	assert.True(t, lz.Lt("d"))
	assert.True(t, lz.Lte("b"))
	assert.True(t, lz.Eq("b"))
	assert.True(t, lz.Ne("a"))
}

func TestHTMLHashMod(t *testing.T) {
	lz := NewLazyStringWithFunc(func() string { return "foo 7" })
	assert.Equal(t, "foo 7", lz.HTML())
	assert.Equal(t, hashString("foo 7"), lz.Hash())
	assert.Equal(t, "foo 7", lz.Mod("s"))
	assert.Equal(t, "bar: foo 7", lz.Format("bar: %s"))
}

func TestGetattrPassthroughAndError(t *testing.T) {
	lz := NewLazyStringWithFunc(func() string { return "abcdef" })
	assert.Equal(t, "ABCDEF", lz.Upper())
}

func TestKwargsArePassed(t *testing.T) {
	f := func(x ...string) string {
		if len(x) > 0 {
			return toUpper(x[0])
		}
		return ""
	}
	lz := NewLazyStringWithFunc(func() string { return f("abc") })
	assert.Equal(t, "ABC", lz.String())
}

func TestEdgeCaseStrConversion(t *testing.T) {
	lz := NewLazyStringWithFunc(func() string { return "123" })
	assert.Equal(t, "123", lz.String())
}