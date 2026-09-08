package original

import (
	"testing"
)

type Calculator struct{}

func (c *Calculator) Add(a, b int) int {
	return a + b
}

// This struct and variable simulate the Java static fields and are reset for test isolation.
type staticCollections struct {
	integerSet  map[int]bool
	integerList []int
}

func newStaticCollections() *staticCollections {
	return &staticCollections{
		integerSet:  map[int]bool{},
		integerList: []int{},
	}
}

func TestRepeatedAddNumber(t *testing.T) {
	c := &Calculator{}
	const repetitions = 5
	for i := 0; i < repetitions; i++ {
		if got := c.Add(1, 1); got != 2 {
			t.Fatalf("repetition %d: 1+1 should equal 2", i+1)
		}
	}
}

func TestRepeatedAddingToCollections(t *testing.T) {
	const repetitions = 5
	coll := newStaticCollections()
	for i := 1; i <= repetitions; i++ {
		coll.integerSet[1] = true
		coll.integerList = append(coll.integerList, i)
		if want := 1; len(coll.integerSet) != want {
			t.Errorf("repetition %d: set should have %d element(s), got %d", i, want, len(coll.integerSet))
		}
		if len(coll.integerList) != i {
			t.Errorf("repetition %d: list should have %d element(s), got %d", i, len(coll.integerList))
		}
	}
}