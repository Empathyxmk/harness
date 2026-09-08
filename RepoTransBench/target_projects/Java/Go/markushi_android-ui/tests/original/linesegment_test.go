package original

import (
	"testing"
	"reflect"
)

type LineSegment struct {
	Indexes []int
}

// Mocks for Java code
func NewLineSegment(values ...int) *LineSegment {
	idx := make([]int, len(values))
	copy(idx, values)
	return &LineSegment{Indexes: idx}
}

func (l *LineSegment) GetStartIdx() int {
	if len(l.Indexes) > 0 {
		return l.Indexes[0]
	}
	return 0
}

// Simulate Android Parceling as byte slice
func (l *LineSegment) WriteToParcel(buf *[]int) {
	*buf = append((*buf)[:0], l.Indexes...)
}

func (l *LineSegment) DescribeContents() int {
	return 0
}

type LineSegmentCreator struct{}

func (c LineSegmentCreator) CreateFromParcel(buf []int) *LineSegment {
	cpy := make([]int, len(buf))
	copy(cpy, buf)
	return &LineSegment{Indexes: cpy}
}

func (c LineSegmentCreator) NewArray(size int) []*LineSegment {
	return make([]*LineSegment, size)
}

var lineSegmentCreator = LineSegmentCreator{}

func TestConstructorAndGetStartIdx(t *testing.T) {
	seg := NewLineSegment(1, 2, 3)
	want := []int{1, 2, 3}
	if !reflect.DeepEqual(seg.Indexes, want) {
		t.Errorf("Indexes = %v; want %v", seg.Indexes, want)
	}
	if seg.GetStartIdx() != 1 {
		t.Errorf("GetStartIdx = %d; want 1", seg.GetStartIdx())
	}
}

func TestParcelableWriteAndRead(t *testing.T) {
	seg := NewLineSegment(4, 5, 6)
	var buf []int
	seg.WriteToParcel(&buf)
	created := lineSegmentCreator.CreateFromParcel(buf)
	want := []int{4, 5, 6}
	if !reflect.DeepEqual(created.Indexes, want) {
		t.Errorf("Parcel/Unparcel Indexes = %v; want %v", created.Indexes, want)
	}
	arr := lineSegmentCreator.NewArray(2)
	if len(arr) != 2 {
		t.Errorf("NewArray(2) has length %d; want 2", len(arr))
	}
}

func TestDescribeContents(t *testing.T) {
	seg := NewLineSegment(1, 2)
	if seg.DescribeContents() != 0 {
		t.Errorf("DescribeContents = %d; want 0", seg.DescribeContents())
	}
}