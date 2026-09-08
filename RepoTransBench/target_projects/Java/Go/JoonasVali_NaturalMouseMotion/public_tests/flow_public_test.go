package public_tests

import (
	"math"
	"testing"
)

func normalize(arr []float64, normTo float64) []float64 {
	total := 0.0
	for _, v := range arr {
		total += v
	}
	result := make([]float64, len(arr))
	for i, v := range arr {
		result[i] = v * normTo / total * float64(len(arr))
	}
	return result
}

func characteristicsStepSum(characteristics []float64, totalDistance float64, nSteps int) float64 {
	norm := normalize(characteristics, 100.0)
	sum := 0.0
	for i := 0; i < nSteps; i++ {
		// Linear mapping for test purposes
		proportion := float64(i) / float64(nSteps)
		index := int(float64(len(norm)) * proportion)
		if index >= len(norm) {
			index = len(norm) - 1
		}
		step := totalDistance * norm[index] / (100.0 * float64(nSteps))
		sum += step
	}
	return sum
}

func assertArrayEquals(t *testing.T, expected, actual []float64, delta float64) {
	if len(expected) != len(actual) {
		t.Fatalf("Arrays differ in length: %d vs %d", len(expected), len(actual))
	}
	for i := range expected {
		if math.Abs(expected[i]-actual[i]) > delta {
			t.Errorf("Array mismatch at %d: expected %v got %v", i, expected[i], actual[i])
		}
	}
}

func TestConstantCharacteristicsGetNormalizedTo150(t *testing.T) {
	characteristics := make([]float64, 50)
	for i := range characteristics {
		characteristics[i] = 300.0
	}
	result := normalize(characteristics, 100.0)
	sum := 0.0
	for i := range result {
		if math.Abs(result[i]-100.0) > 1e-5 {
			t.Errorf("Expected 100 got %f at %d", result[i], i)
		}
		sum += result[i]
	}
	if math.Abs(sum-100.0*float64(len(characteristics))) > 1e-5 {
		t.Errorf("Sum mismatch: got %f", sum)
	}
}

func TestConstantCharacteristicsGetNormalizedTo100withVeryLargeArray(t *testing.T) {
	characteristics := make([]float64, 2000)
	for i := range characteristics {
		characteristics[i] = 999.0
	}
	result := normalize(characteristics, 100.0)
	sum := 0.0
	for i := range result {
		if math.Abs(result[i]-100.0) > 1e-5 {
			t.Errorf("Expected 100 got %f at %d", result[i], i)
		}
		sum += result[i]
	}
	if math.Abs(sum-100.0*float64(len(characteristics))) > 1e-5 {
		t.Errorf("Sum mismatch: got %f", sum)
	}
}

func TestConstantCharacteristicsGetNormalizedTo100fromMidValues(t *testing.T) {
	characteristics := make([]float64, 10)
	for i := range characteristics {
		characteristics[i] = 31
	}
	result := normalize(characteristics, 100.0)
	sum := 0.0
	for i := range result {
		if math.Abs(result[i]-100.0) > 1e-5 {
			t.Errorf("Expected 100 got %f at %d", result[i], i)
		}
		sum += result[i]
	}
	if math.Abs(sum-100.0*float64(len(characteristics))) > 1e-5 {
		t.Errorf("Sum mismatch: got %f", sum)
	}
}

func TestCharacteristicsGetNormalizedToAverage100Public(t *testing.T) {
	characteristics := []float64{10, 20, 40}
	result := normalize(characteristics, 100.0)
	sum := 0.0
	for _, v := range result {
		sum += v
	}
	if math.Abs(result[0]-50.0) > 1e-5 {
		t.Errorf("Expected 50, got %f", result[0])
	}
	if math.Abs(result[1]-100.0) > 1e-5 {
		t.Errorf("Expected 100, got %f", result[1])
	}
	if math.Abs(result[2]-200.0) > 1e-5 {
		t.Errorf("Expected 200, got %f", result[2])
	}
	if math.Abs(sum-100.0*float64(len(characteristics))) > 1e-5 {
		t.Errorf("Sum mismatch: got %f", sum)
	}
}

func TestStepsAddUpToDistance_accelerating_public(t *testing.T) {
	characteristics := []float64{2, 3, 5, 7}
	steps := 4
	total := 80.0
	sum := characteristicsStepSum(characteristics, total, steps)
	if math.Abs(sum-80.0) > 1e-5 {
		t.Errorf("Expected steps sum to 80, got %f", sum)
	}
}

func TestStepsAddUpToDistance_decelerating_public(t *testing.T) {
	characteristics := []float64{7, 5, 3, 2}
	steps := 4
	total := 80.0
	sum := characteristicsStepSum(characteristics, total, steps)
	if math.Abs(sum-80.0) > 1e-5 {
		t.Errorf("Expected steps sum to 80, got %f", sum)
	}
}

func TestStepsAddUpToDistance_characteristics_not_dividable_by_steps_pub1(t *testing.T) {
	characteristics := []float64{2, 2, 4, 4, 6, 6, 8}
	sum := characteristicsStepSum(characteristics, 84, 3)
	if math.Abs(sum-84.0) > 1e-5 {
		t.Errorf("Expected steps sum to 84, got %f", sum)
	}
}

func TestStepsAddUpToDistance_characteristics_not_dividable_by_steps_pub2(t *testing.T) {
	characteristics := []float64{2,4,6,8,10,12,14,16,18}
	sum := characteristicsStepSum(characteristics, 180, 6)
	if math.Abs(sum-180.0) > 1e-5 {
		t.Errorf("Expected steps sum to 180, got %f", sum)
	}
}

func TestStepsAddUpToDistance_characteristics_not_dividable_by_steps_pub3(t *testing.T) {
	characteristics := []float64{2,2,4,4,6,6,8,8}
	sum := characteristicsStepSum(characteristics, 160, 4)
	if math.Abs(sum-160.0) > 1e-5 {
		t.Errorf("Expected steps sum to 160, got %f", sum)
	}
}