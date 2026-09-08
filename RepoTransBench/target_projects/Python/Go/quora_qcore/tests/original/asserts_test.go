package tests

import (
	"testing"
)

func TestAssertEq(t *testing.T) {
	assertEq(t, 2, 2)
	assertEq(t, "foo", "foo")
	assertEq(t, []int{1, 2}, []int{1, 2})
}

func TestAssertNe(t *testing.T) {
	assertNe(t, 1, 2)
	assertNe(t, "foo", "bar")
	assertNe(t, []int{1, 2}, []int{2, 1})
}

func TestAssertTrueFalse(t *testing.T) {
	assertTrue(t, 1 < 2)
	assertFalse(t, 2 < 1)
}

func TestAssertPanic(t *testing.T) {
	assertPanic(t, func() {
		panic("trigger panic")
	})
}

func TestAssertNoPanic(t *testing.T) {
	assertNoPanic(t, func() {})
}