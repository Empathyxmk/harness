package public_tests

import (
	"testing"

	"github.com/example/nickjj_ansible_docker/tests"
)

func TestIncrementPublic(t *testing.T) {
	if tests.Increment(10) != 11 {
		t.Errorf("Increment(10) should be 11")
	}
	if tests.Increment(-4) != -3 {
		t.Errorf("Increment(-4) should be -3")
	}
}

func TestSumPublic(t *testing.T) {
	if tests.Total([]int{3, 8, 12}) != 23 {
		t.Errorf("Total([3,8,12]) should be 23")
	}
	if tests.Total([]int{}) != 0 {
		t.Errorf("Total([]) should be 0")
	}
	if tests.Total([]int{-2, 5}) != 3 {
		t.Errorf("Total([-2,5]) should be 3")
	}
}

func TestIsEvenPublic(t *testing.T) {
	if !tests.IsEven(100) {
		t.Errorf("IsEven(100) should be true")
	}
	if tests.IsEven(15) {
		t.Errorf("IsEven(15) should be false")
	}
	if !tests.IsEven(-22) {
		t.Errorf("IsEven(-22) should be true")
	}
}

func TestCustomCasePublic(t *testing.T) {
	numbers := []int{6, 7, 8, 9}
	evenCount := 0
	for _, n := range numbers {
		if tests.IsEven(n) {
			evenCount++
		}
	}
	if evenCount != 2 {
		t.Errorf("Even count in [6,7,8,9] should be 2, got %v", evenCount)
	}
}

func TestZeroIncrementPublic(t *testing.T) {
	if tests.Increment(0) != 1 {
		t.Errorf("Increment(0) should be 1")
	}
}

func TestNegativeTotalPublic(t *testing.T) {
	if tests.Total([]int{-5, -5, -10}) != -20 {
		t.Errorf("Total([-5, -5, -10]) should be -20")
	}
}