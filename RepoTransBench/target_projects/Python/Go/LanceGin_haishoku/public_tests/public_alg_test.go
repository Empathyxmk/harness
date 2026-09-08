package public_tests

import (
	"reflect"
	"testing"
	"lancegin_haishoku/haishoku/alg"
)

func TestRgb2hlsVariation(t *testing.T) {
	result := alg.Rgb2hls([3]int{200, 150, 100})
	want := [3]int{30, 150, 102}
	if !reflect.DeepEqual(result, want) {
		t.Errorf("Rgb2hls((200,150,100)) = %v; want %v", result, want)
	}
}

func TestGetHistogramVariation(t *testing.T) {
	input := [][3]int{{100, 100, 100}, {100, 100, 100}, {50, 50, 50}}
	got := alg.GetHistogram(input)
	want := map[[3]int]int{
		{100, 100, 100}: 2,
		{50, 50, 50}:    1,
	}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("GetHistogram got %v, want %v", got, want)
	}
}