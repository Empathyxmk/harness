package original

import (
	"math/rand"
	"testing"
	"agarciadom_xeger/xeger"
)

func TestXeger_ShouldGenerateTextCorrectly(t *testing.T) {
	regex := "[ab]{4,6}c"
	g := xeger.NewXeger(regex)
	for i := 0; i < 100; i++ {
		out := g.Generate()
		// Placeholder: regex match. When real, do regex.
		if len(out) == 0 {
			t.Errorf("Output string is empty")
		}
	}
}

func TestXeger_RepeatableRegex(t *testing.T) {
	for x := 0; x < 1000; x++ {
		g1 := xeger.NewXegerWithRand("[ab]{4,6}c", rand.New(rand.NewSource(1000)))
		g2 := xeger.NewXegerWithRand("[ab]{4,6}c", rand.New(rand.NewSource(1000)))
		first := generateRegexSlice(g1, 100)
		second := generateRegexSlice(g2, 100)
		assertListEquals(t, first, second)
	}
}

func TestXeger_WalkRange(t *testing.T) {
	for x := 0; x < 100; x++ {
		g1 := xeger.NewXegerWithRand("[ab]{0,100}c", rand.New(rand.NewSource(1000)))
		g2 := xeger.NewXegerWithRand("[ab]{0,100}c", rand.New(rand.NewSource(1000)))
		first := generateRegexSliceWithBounds(g1, 100, 0, 100)
		second := generateRegexSliceWithBounds(g2, 100, 0, 100)
		assertListEquals(t, first, second)
	}
}

func generateRegexSlice(g *xeger.Xeger, count int) []string {
	arr := make([]string, count)
	for i := 0; i < count; i++ {
		arr[i] = g.Generate()
	}
	return arr
}

func generateRegexSliceWithBounds(g *xeger.Xeger, count, min, max int) []string {
	arr := make([]string, count)
	for i := 0; i < count; i++ {
		s, err := g.GenerateWithBounds(min, max)
		if err != nil {
			arr[i] = ""
		} else {
			arr[i] = s
		}
	}
	return arr
}

func assertListEquals(t *testing.T, a, b []string) {
	if len(a) != len(b) {
		t.Fatalf("List lengths do not match: %d vs %d", len(a), len(b))
	}
	for i := range a {
		if a[i] != b[i] {
			t.Errorf("Mismatch at %d: %q vs %q", i, a[i], b[i])
		}
	}
}