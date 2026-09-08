package public_tests

import (
	"testing"
)

type LogFileItem struct {
	LogFileName     string
	FullLogFileName string
	CurrLogSize     int
	CurrLogBuff     byte
	AlLogBufA       []*BufferStub
	AlLogBufB       []*BufferStub
	NextWriteTime   int
	LastPCDate      string
	CurrCacheSize   int
}

type BufferStub struct {
	Data string
}

func NewLogFileItem() *LogFileItem {
	return &LogFileItem{
		LogFileName:     "",
		FullLogFileName: "",
		CurrLogSize:     0,
		CurrLogBuff:     'A',
		AlLogBufA:       []*BufferStub{},
		AlLogBufB:       []*BufferStub{},
		NextWriteTime:   0,
		LastPCDate:      "",
		CurrCacheSize:   0,
	}
}

func TestLogFileItemFieldsWithDifferentData(t *testing.T) {
	lfi := NewLogFileItem()
	if lfi.LogFileName != "" {
		t.Errorf("Expected LogFileName '', got '%s'", lfi.LogFileName)
	}
	if lfi.FullLogFileName != "" {
		t.Errorf("Expected FullLogFileName '', got '%s'", lfi.FullLogFileName)
	}
	if lfi.CurrLogSize != 0 {
		t.Errorf("Expected CurrLogSize 0, got %d", lfi.CurrLogSize)
	}
	if lfi.CurrLogBuff != 'A' {
		t.Errorf("Expected CurrLogBuff 'A', got %c", lfi.CurrLogBuff)
	}
	if lfi.AlLogBufA == nil {
		t.Error("AlLogBufA should not be nil")
	}
	if lfi.AlLogBufB == nil {
		t.Error("AlLogBufB should not be nil")
	}
	if len(lfi.AlLogBufA) != 0 {
		t.Errorf("AlLogBufA should be empty at init")
	}
	if len(lfi.AlLogBufB) != 0 {
		t.Errorf("AlLogBufB should be empty at init")
	}
	if lfi.NextWriteTime != 0 {
		t.Errorf("Expected NextWriteTime = 0")
	}
	if lfi.LastPCDate != "" {
		t.Errorf("Expected LastPCDate is empty, got %q", lfi.LastPCDate)
	}
	if lfi.CurrCacheSize != 0 {
		t.Errorf("Expected CurrCacheSize 0")
	}
	lfi.AlLogBufA = append(lfi.AlLogBufA, &BufferStub{Data: "public test AAA"})
	lfi.AlLogBufB = append(lfi.AlLogBufB, &BufferStub{Data: "public test BBB"})
	lfi.AlLogBufA = append(lfi.AlLogBufA, &BufferStub{Data: "extra item in A"})
	if len(lfi.AlLogBufA) != 2 {
		t.Errorf("Expected AlLogBufA length 2 after adding, got %d", len(lfi.AlLogBufA))
	}
	if len(lfi.AlLogBufB) != 1 {
		t.Errorf("Expected AlLogBufB length 1 after adding, got %d", len(lfi.AlLogBufB))
	}
	if lfi.AlLogBufA[0].Data != "public test AAA" {
		t.Errorf("First log buf A should be 'public test AAA'")
	}
	if lfi.AlLogBufB[0].Data != "public test BBB" {
		t.Errorf("First log buf B should be 'public test BBB'")
	}
	if lfi.AlLogBufA[1].Data != "extra item in A" {
		t.Errorf("Second log buf A should be 'extra item in A'")
	}
}