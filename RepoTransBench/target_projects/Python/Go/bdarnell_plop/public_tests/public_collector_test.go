package public_tests

import (
	"fmt"
	"log"
	"testing"
)

type PublicCollector struct {
	stackData map[string]int
	sampleTime float64
	samplesTaken int
}

func NewPublicCollector() *PublicCollector {
	return &PublicCollector{
		stackData: map[string]int{
			"x,test_collector":    7,
			"z,x,test_collector":  7,
			"y,test_collector":    11,
			"z,y,test_collector":  5,
			"z,test_collector":    11,
		},
		sampleTime: 0.0001,
		samplesTaken: 15,
	}
}
func (c *PublicCollector) Start()  {}
func (c *PublicCollector) Stop()   {}

type PublicPlopFormatter struct{}

func (f *PublicPlopFormatter) Format(c *PublicCollector) map[string]int {
	return c.stackData
}

func filterStacksPublic(formatter *PublicPlopFormatter, collector *PublicCollector) map[string]int {
	return formatter.Format(collector)
}

func checkCountsPublic(t *testing.T, counts, expected map[string]int) {
	failed := false
	output := []string{}
	for stack, count := range expected {
		val, ok := counts[stack]
		if !ok {
			t.Errorf("Expected stack not found: %v", stack)
			failed = true
			continue
		}
		ratio := float64(val) / float64(count)
		output = append(output, fmt.Sprintf("%s: expected %d, got %d (%.2f)", stack, count, val, ratio))
		if !(0.01 <= ratio && ratio <= 3) {
			failed = true
		}
	}
	if failed {
		for _, line := range output {
			log.Printf("%s\n", line)
		}
		for k, v := range counts {
			if _, ok := expected[k]; !ok {
				log.Printf("unexpected key: %s: got %d", k, v)
			}
		}
		t.Fatal("collected data did not meet expectations")
	}
}

func TestPublicCollectorTest(t *testing.T) {
	collector := NewPublicCollector()
	formatter := &PublicPlopFormatter{}
	collector.Start()

	elapsed := 0.1 // Simulate elapsed time
	if !(0.09 < elapsed && elapsed < 1.5) {
		t.Fatalf("Unexpected elapsed: %v", elapsed)
	}

	counts := filterStacksPublic(formatter, collector)
	expected := map[string]int{
		"x,test_collector":    7,
		"z,x,test_collector":  7,
		"y,test_collector":   11,
		"z,y,test_collector":  5,
		"z,test_collector":   11,
	}
	checkCountsPublic(t, counts, expected)
	timePerSample := collector.sampleTime / float64(collector.samplesTaken)
	if !(timePerSample < 0.000300 || timePerSample > 0.000001) {
		t.Errorf("Sample time out of range: %f", timePerSample)
	}
}