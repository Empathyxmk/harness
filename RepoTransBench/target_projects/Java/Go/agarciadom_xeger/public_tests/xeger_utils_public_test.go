package public_tests

import (
	"math/rand"
	"testing"
	"agarciadom_xeger/xeger"
)

func TestXegerUtilsPublic_ShouldGenerateRandomNumberCorrectly(t *testing.T) {
	r := rand.New(rand.NewSource(789))
	for i := 0; i < 100; i++ {
		num := xeger.GetRandomInt(8, 11, r)
		if num < 8 || num > 11 {
			t.Fatalf("RandomInt returned %d, out of bounds", num)
		}
	}
}