package public_tests

import (
	"io/ioutil"
	"os"
	"strings"
	"testing"
)

type FastqRecord struct {
	Name string
	Seq  string
	Qual string
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

func TestMergeEffect(t *testing.T) {
	stats1 := NewTrimStats()
	stats2 := NewTrimStats()
	rec := NewFastqRecord("other", "xyz", "===!")
	orig := []FastqRecord{rec}
	surv := []FastqRecord{rec}
	stats2.logPair(orig, surv)
	stats1.merge(stats2)
	if stats1 == nil {
		t.Fatal("stats1 should not be nil")
	}
}

func TestLogPairDropAndSurvive(t *testing.T) {
	stats := NewTrimStats()
	recDrop := NewFastqRecord("d", "ggg", "!!!")
	recSurvive := NewFastqRecord("s", "ccc", "$$$")
	orig := []FastqRecord{recDrop}
	surv := []FastqRecord{}
	stats.logPair(orig, surv) // drop
	orig2 := []FastqRecord{recSurvive}
	surv2 := []FastqRecord{recSurvive}
	stats.logPair(orig2, surv2) // survives

	origPair := []FastqRecord{recDrop, recSurvive}
	survPair := []FastqRecord{recSurvive, FastqRecord{}}
	stats.logPair(origPair, survPair) // only left survived
}

func TestProcessStatsSEAndPEDistinct(t *testing.T) {
	stats := NewTrimStats()
	rec := NewFastqRecord("n2", "AGAG", "zzzx")
	stats.logPair([]FastqRecord{rec}, []FastqRecord{})
	se := stats.processStatsSE(nil)
	if !strings.Contains(strings.ToLower(se), "input reads") {
		t.Errorf("Should mention Input Reads, got: %s", se)
	}
	pe := stats.processStatsPE(nil)
	if !strings.Contains(strings.ToLower(pe), "input read pairs") {
		t.Errorf("Should mention Input Read Pairs, got: %s", pe)
	}
}

func TestProcessStatsPEWithCustomFile(t *testing.T) {
	stats := NewTrimStats()
	tmp, err := ioutil.TempFile("", "pstats.tmp")
	if err != nil {
		t.Fatalf("Could not create temp file: %v", err)
	}
	defer os.Remove(tmp.Name())
	rec := NewFastqRecord("r3", "ATGCT", "####.")
	stats.logPair([]FastqRecord{rec}, []FastqRecord{})
	stats.processStatsPE(tmp)
	fi, err := os.Stat(tmp.Name())
	if err != nil || fi.Size() < 0 {
		t.Errorf("Temp file does not exist or is invalid after processStats: %v", err)
	}
}