package original

import (
	"fmt"
	"testing"
	"time"
)
import drawille "github.com/example/asciimoo_drawille"

func TestSpeed(t *testing.T) {
	c := drawille.NewCanvas()
	frames := 1000 * 10

	sizes := [][2]int{
		{0, 0},
		{10, 10},
		{20, 20},
		{20, 40},
		{40, 20},
		{40, 40},
		{100, 100},
	}

	for _, size := range sizes {
		x, y := size[0], size[1]
		c.Set(0, 0)
		for i := 0; i < y; i++ {
			c.Set(x, i)
		}
		start := time.Now()
		for i := 0; i < frames; i++ {
			c.Frame()
		}
		elapsed := time.Since(start)
		fmt.Printf("%dx%d\t%v\n", x, y, elapsed)
		c.Clear()
	}
}