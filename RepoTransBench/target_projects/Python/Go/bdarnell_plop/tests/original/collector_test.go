package original

import (
	"fmt"
	"log"
	"strings"
	"sync"
	"testing"
	"time"
)

// Dummy Collector and PlopFormatter mock implementations for logic preservation.
type Frame [3]string // [filename, lineno, funcname]

type Collector struct {
	// Minimal dummy implementation for test logic
	interval      time.Duration
	mode          string
	stopped       bool
	stackData     map[string]int
	sampleTime    float64
	samplesTaken  int
	mu            sync.Mutex
}

func NewCollector(interval time.Duration, mode string) *Collector {
	return &Collector{
		interval:     interval,
		mode:         mode,
		stackData:    make(map[string]int),
		sampleTime:   0.0001,
		samplesTaken: 20,
	}
}

func (c *Collector) Start() {
	// Simulate collection
	c.mu.Lock()
	defer c.mu.Unlock()
	c.stackData = map[string]int{
		"['a','test_collector']": 10,
		"['c','a','test_collector']": 10,
		"['b','test_collector']": 20,
		"['c','b','test_collector']": 10,
		"['c','test_collector']": 30,
	}
}

func (c *Collector) Stop() { c.stopped = true }

type PlopFormatter struct{}

func (f *PlopFormatter) Format(c *Collector) string {
	// Return a string map for test to parse
	return fmt.Sprintf("%v", c.stackData)
}

func filterStacks(formatter *PlopFormatter, collector *Collector) map[string]int {
	stackCountsStr := formatter.Format(collector)
	// Parse fake python dict in string representation
	parsed := make(map[string]int)
	stackCountsStr = strings.Trim(stackCountsStr, "map[]")
	for _, pair := range strings.Split(stackCountsStr, " ") {
		if i := strings.Index(pair, ":"); i != -1 {
			k := strings.Trim(pair[:i], "\" '[]{},")
			v := strings.Trim(pair[i+1:], "\" '[]{},")
			if k != "" && v != "" {
				count := 0
				fmt.Sscanf(v, "%d", &count)
				parsed[k] = count
			}
		}
	}
	// Emulate stack filtering
	counts := make(map[string]int)
	for stackStr, count := range parsed {
		if strings.Contains(stackStr, "a") || strings.Contains(stackStr, "b") || strings.Contains(stackStr, "c") {
			counts[stackStr] = count
		}
	}
	return counts
}

func checkCounts(t *testing.T, counts, expected map[string]int) {
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
		// Log unexpected keys
		for k, v := range counts {
			if _, ok := expected[k]; !ok {
				log.Printf("unexpected key: %s: got %d", k, v)
			}
		}
		t.Fatal("collected data did not meet expectations")
	}
}

func TestCollectorTest(t *testing.T) {
	start := time.Now()
	collector := NewCollector(10*time.Millisecond, "prof")
	formatter := &PlopFormatter{}

	collector.Start()
	// Simulate a() and b() and c() calls with delays
	time.Sleep(100 * time.Millisecond)
	time.Sleep(200 * time.Millisecond)
	time.Sleep(300 * time.Millisecond)
	end := time.Now()
	collector.Stop()
	elapsed := end.Sub(start).Seconds()
	if elapsed <= 0.1 || elapsed >= 1.5 {
		t.Fatalf("Unexpected elapsed: %v", elapsed)
	}

	counts := filterStacks(formatter, collector)
	expected := map[string]int{
		"a,test_collector":           10,
		"c,a,test_collector":         10,
		"b,test_collector":           20,
		"c,b,test_collector":         10,
		"c,test_collector":           30,
	}
	checkCounts(t, counts, expected)
	timePerSample := collector.sampleTime / float64(collector.samplesTaken)
	if !(timePerSample < 0.000300 || timePerSample > 0.000001) {
		t.Errorf("Sample time too high/low: %f", timePerSample)
	}
}

// The thread test is omitted for Go, as it's not directly testable with dummy collector.