package public_tests

import (
	"reflect"
	"testing"
	"lancegin_haishoku/haishoku/alg"
)

func TestRgb2hlsBoundary(t *testing.T) {
	if !reflect.DeepEqual(alg.Rgb2hls([3]int{0, 0, 0}), [3]int{0, 0, 0}) {
		t.Errorf("Rgb2hls((0,0,0)) wrong")
	}
	if !reflect.DeepEqual(alg.Rgb2hls([3]int{255, 255, 255}), [3]int{0, 255, 0}) {
		t.Errorf("Rgb2hls((255,255,255)) wrong")
	}
}