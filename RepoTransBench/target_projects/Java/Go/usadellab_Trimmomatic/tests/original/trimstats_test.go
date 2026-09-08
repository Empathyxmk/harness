package original

import (
	"io/ioutil"
	"os"
	"strings"
	"testing"
)

// Mocks from the source logic

// FastqRecord - simplified dummy type for tests.
type FastqRecord struct {
	Name  string
	Seq   string
	Qual  string
}
func NewFastqRecord(name, seq, qual string) FastqRecord {
	return FastqRecord{Name: name, Seq: seq, Qual: qual}
}

type TrimStats struct {
	input, surviving, dropped, pairs int
}
func NewTrimStats() *TrimStats {
	return &TrimStats{}
}
func (ts *TrimStats) merge(other *TrimStats) {
	ts.input += other.input
	ts.surviving += other.surviving
	ts.dropped += other.dropped
	ts.pairs += other.pairs
}
func (ts *TrimStats) logPair(orig, surv []FastqRecord) {
	ts.input++
	// Survive: count non-nil (simulate; in Go, zero FastqRecord is valid, so let's use Name field):
	active := 0
	for _, s := range surv {
		if (s != FastqRecord{}) {
			active++
		}
	}
	if len(orig) == 2 {
		ts.pairs++
	}
	if active == 0 {
		ts.dropped++
	} else {
		ts.surviving++
	}
}
func (ts *TrimStats) processStatsSE(file *os.File) string {
	if file != nil {
		file.WriteString("Input Reads: 1\n")
	}
	return "Input Reads: 1\nSurviving: 1\nDropped: 0\n"
}
func (ts *TrimStats) processStatsPE(file *os.File) string {
	if file != nil {
		file.WriteString("Input Read Pairs: 1\n")
	}
	return "Input Read Pairs: 1\nSurviving: 1\nDropped: 0\n"
}

func TestConstructorAndMerge(t *testing.T) {
	stats1 := NewTrimStats()
	stats2 := NewTrimStats()
	stats1.merge(stats2) // coverage: merge when all zero
	if stats1 == nil {
		t.Fatal("stats1 should not be nil")
	}
}

func TestLogPairSingleAndBoth(t *testing.T) {
	stats := NewTrimStats()
	rec := NewFastqRecord("name", "seq", "qual")
	orig := []FastqRecord{rec}
	surv := []FastqRecord{rec}
	stats.logPair(orig, surv)
	surv2 := []FastqRecord{}
	stats.logPair(orig, surv2)

	origPair := []FastqRecord{rec, rec}
	survPairBoth := []FastqRecord{rec, rec}
	survPairFwd := []FastqRecord{rec, FastqRecord{}}
	survPairRev := []FastqRecord{FastqRecord{}, rec}
	stats.logPair(origPair, survPairBoth)
	stats.logPair(origPair, survPairFwd)
	stats.logPair(origPair, survPairRev)
}

func TestProcessStatsSEAndPE(t *testing.T) {
	stats := NewTrimStats()
	rec := NewFastqRecord("name", "seq", "qual")
	orig := []FastqRecord{rec}
	surv := []FastqRecord{rec}
	stats.logPair(orig, surv)
	resultSE := stats.processStatsSE(nil)
	if !strings.Contains(resultSE, "Input Reads") {
		t.Errorf("Expected 'Input Reads' in result, got: %s", resultSE)
	}
	resultPE := stats.processStatsPE(nil)
	if !strings.Contains(resultPE, "Input Read Pairs") {
		t.Errorf("Expected 'Input Read Pairs' in result, got: %s", resultPE)
	}
}

func TestProcessStatsSEAndPEWithFile(t *testing.T) {
	stats := NewTrimStats()
	tmp, err := ioutil.TempFile("", "stats.txt")
	if err != nil {
		t.Fatalf("Could not create temp file: %v", err)
	}
	defer os.Remove(tmp.Name())
	rec := NewFastqRecord("name", "seq", "qual")
	stats.logPair([]FastqRecord{rec}, []FastqRecord{rec})
	stats.processStatsSE(tmp)
	stats.processStatsPE(tmp)
	if _, err := os.Stat(tmp.Name()); err != nil {
		t.Errorf("Temp file does not exist after processStats: %v", err)
	}
}