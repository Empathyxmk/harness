package original

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

type PC1 struct {
	X int
	Y string
}

type PC2 struct {
	ListOfC1 []PC1
}

type PC3 struct {
	ListOfC2 []PC2
}

func createPC3(len1, len2 int) *PC3 {
	listOfC1 := make([]PC1, len1)
	for i := 0; i < len1; i++ {
		listOfC1[i] = PC1{i, string(rune('0' + i%10))}
	}
	listOfC2 := make([]PC2, len2)
	for i := 0; i < len2; i++ {
		// Don't duplicate C1s in memory so we use same slice reference (for perf)
		listOfC2[i] = PC2{listOfC1}
	}
	return &PC3{listOfC2}
}

var _c3_1 *PC3
var _c3_2 *PC3
var _c3_3 *PC3

func TestMain(m *testing.M) {
	_c3_1 = createPC3(100, 10)
	_c3_2 = createPC3(100, 100)
	_c3_3 = createPC3(100, 1000)
	m.Run()
}

func _doTestDump(t *testing.T, timeLimit float64, strict bool) {
	start1 := time.Now()
	if strict {
		jsons.DumpStrict(_c3_1)
	} else {
		jsons.Dump(_c3_1)
	}
	elapsed1 := time.Since(start1).Seconds()

	start2 := time.Now()
	if strict {
		jsons.DumpStrict(_c3_2)
	} else {
		jsons.Dump(_c3_2)
	}
	elapsed2 := time.Since(start2).Seconds()

	start3 := time.Now()
	if strict {
		jsons.DumpStrict(_c3_3)
	} else {
		jsons.Dump(_c3_3)
	}
	elapsed3 := time.Since(start3).Seconds()

	assert.Truef(t, elapsed3 < timeLimit, "The operation took %.4f seconds", elapsed3)

	avg1 := elapsed1 / 10.0
	avg2 := elapsed2 / 100.0
	avg3 := elapsed3 / 1000.0
	threshold := 0.1
	linearScaling := (abs(avg2-avg1) < threshold) && (abs(avg3-avg2) < threshold)
	assert.Truef(t, linearScaling,
		"Non-linear dump scaling: delta(avg2-avg1)=%.4f, delta(avg3-avg2)=%.4f", abs(avg2-avg1), abs(avg3-avg2))
}

func abs(a float64) float64 {
	if a < 0 {
		return -a
	}
	return a
}

func TestPerformanceDump(t *testing.T) {
	_doTestDump(t, 16.0, false)
}

func TestPerformanceDumpStrict(t *testing.T) {
	_doTestDump(t, 8.0, true)
}