package original

import (
	"fmt"
	"testing"
)

func checkSorted(cards []int) bool {
	for i := 0; i < len(cards)-1; i++ {
		if cards[i] >= cards[i+1] {
			return false
		}
	}
	return true
}

// Simulates selectionSort, insertionSort, mergeSort
func selectionSort(cards []int) []int {
	for i := 0; i < len(cards); i++ {
		minIdx := i
		for j := i + 1; j < len(cards); j++ {
			if cards[j] < cards[minIdx] {
				minIdx = j
			}
		}
		cards[i], cards[minIdx] = cards[minIdx], cards[i]
	}
	return cards
}
func insertionSort(cards []int) []int {
	for i := 1; i < len(cards); i++ {
		j := i
		for j > 0 && cards[j-1] > cards[j] {
			cards[j-1], cards[j] = cards[j], cards[j-1]
			j--
		}
	}
	return cards
}
func mergeSort(cards []int) []int {
	if len(cards) <= 1 {
		return cards
	}
	mid := len(cards) / 2
	left := mergeSort(cards[:mid])
	right := mergeSort(cards[mid:])
	return merge(left, right)
}
func merge(left, right []int) []int {
	result := []int{}
	for len(left) > 0 && len(right) > 0 {
		if left[0] < right[0] {
			result = append(result, left[0])
			left = left[1:]
		} else {
			result = append(result, right[0])
			right = right[1:]
		}
	}
	result = append(result, left...)
	result = append(result, right...)
	return result
}

func TestSortingDeck(t *testing.T) {
	deck := []int{52, 23, 41, 16, 7, 44, 2, 25, 31, 11, 19, 35}
	fmt.Println("Testing selection...")
	sorted := selectionSort(append([]int{}, deck...))
	if !checkSorted(sorted) {
		t.Errorf("Selection sort did not sort deck")
	}

	fmt.Println("Testing mergesort...")
	deck = []int{52, 23, 41, 16, 7, 44, 2, 25, 31, 11, 19, 35}
	msorted := mergeSort(deck)
	if !checkSorted(msorted) {
		t.Errorf("Merge sort did not sort deck")
	}

	fmt.Println("Testing insertion...")
	deck = []int{52, 23, 41, 16, 7, 44, 2, 25, 31, 11, 19, 35}
	isorted := insertionSort(deck)
	if !checkSorted(isorted) {
		t.Errorf("Insertion sort did not sort deck")
	}
}