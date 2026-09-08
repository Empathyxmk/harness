package public_tests

import (
	"testing"
	"reflect"
	"markushi_android_ui/tests/original"
)

func TestConstructorAndGetStartIdxPublic(t *testing.T) {
	seg := original.NewLineSegment(10, 20, 30)
	want := []int{10, 20, 30}
	if !reflect.DeepEqual(seg.Indexes, want) {
		t.Errorf("Indexes = %v; want %v", seg.Indexes, want)
	}
	if seg.GetStartIdx() != 10 {
		t.Errorf("GetStartIdx = %d; want 10", seg.GetStartIdx())
	}
}

func TestParcelableWriteAndReadPublic(t *testing.T) {
	seg := original.NewLineSegment(7, 8, 9)
	var buf []int
	seg.WriteToParcel(&buf)
	created := original.LineSegmentCreator{}.CreateFromParcel(buf)
	want := []int{7, 8, 9}
	if !reflect.DeepEqual(created.Indexes, want) {
		t.Errorf("Parcel/Unparcel Indexes = %v; want %v", created.Indexes, want)
	}
	arr := original.LineSegmentCreator{}.NewArray(3)
	if len(arr) != 3 {
		t.Errorf("NewArray(3) has length %d; want 3", len(arr))
	}
}

func TestDescribeContentsPublic(t *testing.T) {
	seg := original.NewLineSegment(4, 8)
	if seg.DescribeContents() != 0 {
		t.Errorf("DescribeContents = %d; want 0", seg.DescribeContents())
	}
}