package original

import (
	"math/rand"
	"testing"
	"agarciadom_xeger/xeger"
)

func TestXegerUtils_ShouldGenerateRandomNumberCorrectly(t *testing.T) {
	r := rand.New(rand.NewSource(123))
	for i := 0; i < 100; i++ {
		num := xeger.GetRandomInt(3, 7, r)
		if num < 3 || num > 7 {
			t.Fatalf("RandomInt returned %d, out of bounds", num)
		}
	}
}