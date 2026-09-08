package original

import (
	"testing"
	"errors"
	"math"
	"reflect"
)

// ---- Dummy Go OPE types to allow compilation ---
// These MUST be replaced with your real implementation for full test coverage!
type ValueRange struct {
	start int64
	end   int64
}

func NewValueRange(start, end int64) (*ValueRange, error) {
	if reflect.TypeOf(start).Kind() != reflect.Int64 || reflect.TypeOf(end).Kind() != reflect.Int64 {
		return nil, errors.New("InvalidRangeLimitsError")
	}
	return &ValueRange{start: start, end: end}, nil
}

func (vr *ValueRange) size() int64 {
	return vr.end - vr.start
}

func (vr *ValueRange) contains(v int64) bool {
	return v >= vr.start && v <= vr.end
}

// We'll suppose OPE API for the purposes of this test file
type OPE struct {
	key      []byte
	inRange  *ValueRange
	outRange *ValueRange
}

func NewOPE(key []byte, inRange *ValueRange, outRange *ValueRange) *OPE {
	if inRange != nil && outRange != nil && (inRange.size() != outRange.size()) {
		// in real pyope, would panic here
	}
	return &OPE{key: key, inRange: inRange, outRange: outRange}
}
func (o *OPE) encrypt(val int64) int64 {
	// Dummy: just add 1 for demonstration, NOT actual OPE
	return val
}
func (o *OPE) decrypt(val int64) int64 {
	return val
}

// ---- End Dummy Types ----

func TestOrderGuarantees(t *testing.T) {
	values := []int64{0, 1, 2, 10, 28, 42, 1000, 1001, int64(math.Pow(2, 15)) - 1}
	key := []byte("key")
	cipher := NewOPE(key, nil, nil)

	encryptedVals := make([]int64, len(values))
	for i, v := range values {
		encryptedVals[i] = cipher.encrypt(v)
	}
	for i := 1; i < len(encryptedVals); i++ {
		if encryptedVals[i-1] > encryptedVals[i] {
			t.Errorf("Encrypted values not in order: %v", encryptedVals)
		}
	}
}

func TestOpeEncryptDecrypt(t *testing.T) {
	values := []int64{-1000, -100, -20, -1, 0, 1, 10, 100, 314, 1337, 1338, 10000}
	key := []byte("key")
	inRange, _ := NewValueRange(-1000, int64(math.Pow(2, 20)))
	outRange, _ := NewValueRange(-10000, int64(math.Pow(2, 32)))
	cipher := NewOPE(key, inRange, outRange)
	encryptedVals := make([]int64, len(values))
	for i, v := range values {
		encryptedVals[i] = cipher.encrypt(v)
	}
	cipherDec := NewOPE(key, inRange, outRange)
	for i, encrypted := range encryptedVals {
		decrypted := cipherDec.decrypt(encrypted)
		if decrypted != values[i] {
			t.Errorf("Encrypt-decrypt mismatch: input=%d, got=%d", values[i], decrypted)
		}
	}
}

func TestOpeDeterministic(t *testing.T) {
	values := []int64{0, 314, 1337, 1338, 10000}
	cipher := NewOPE([]byte("key-la-la"), nil, nil)
	encFirst := make([]int64, len(values))
	encSecond := make([]int64, len(values))
	for i, v := range values {
		encFirst[i] = cipher.encrypt(v)
	}
	for i, v := range values {
		encSecond[i] = cipher.encrypt(v)
	}
	for i := range encFirst {
		if encFirst[i] != encSecond[i] {
			t.Errorf("Deterministic check failed")
		}
	}
}

func TestDenseRange(t *testing.T) {
	rangeStart := int64(0)
	rangeEnd := int64(math.Pow(2, 15))
	inRange, _ := NewValueRange(rangeStart, rangeEnd)
	outRange, _ := NewValueRange(rangeStart, rangeEnd)
	key := []byte("123")
	cipher := NewOPE(key, inRange, outRange)
	values := []int64{0, 10, 20, 50, 100, 1000, int64(math.Pow(2, 10)), int64(math.Pow(2, 15))}
	for _, v := range values {
		if cipher.encrypt(v) != v {
			t.Errorf("Dense mapping incorrect")
		}
		if cipher.decrypt(v) != v {
			t.Errorf("Dense mapping incorrect (decrypt)")
		}
	}
	_, err := NewValueRange(0, 10)
	outRange2, _ := NewValueRange(1, 2)
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Dense range mismatch did not cause error")
		}
	}()
	NewOPE(key, inRange, outRange2)
}

func TestLongDifferentKeys(t *testing.T) {
	key1 := []byte{0x12, 0x23, 0x34, 0x45, 0x56, 0x67, 0x78, 0x89, 0x90, 0x0A, 0xAB, 0xBC, 0xCD, 0xDE, 0xEF, 0xF0, 0x13, 0x14, 0x15, 0x16}
	key2 := []byte{0x0A, 0xAB, 0xBC, 0xCD, 0xDE, 0xEF, 0xF0, 0x13, 0x14, 0x15, 0x16, 0x12, 0x23, 0x34, 0x45, 0x56, 0x67, 0x78, 0x89, 0x90, 0x12, 0x13}
	ope1 := NewOPE(key1, nil, nil)
	ope2 := NewOPE(key2, nil, nil)
	values := []int64{0, 1, 10, 100, 1000, 2000, 3000, 4000, 5000}
	for _, v := range values {
		if ope1.encrypt(v) == ope2.encrypt(v) {
			t.Errorf("Encrypt with different keys produced same result for v=%d", v)
		}
	}
}

func TestEncryptSmallOutRangeIssue(t *testing.T) {
	key := []byte("fresh key")
	inRange, _ := NewValueRange(0, 2)
	outRange, _ := NewValueRange(2, 5)
	cipher := NewOPE(key, inRange, outRange)
	if cipher.encrypt(0) == 0 {
		t.Errorf("Encrypt value should not be identity in general")
	}
	_ = cipher.encrypt(1)
	_ = cipher.encrypt(2)
}

func TestBigRanges(t *testing.T) {
	inRange, _ := NewValueRange(int64(math.Pow(2, 32)), int64(math.Pow(2, 33)))
	outRange, _ := NewValueRange(int64(math.Pow(2, 48)), int64(math.Pow(2, 49)))
	ope := NewOPE([]byte("test-big-ranges"), inRange, outRange)
	plaintext := inRange.start
	for plaintext <= inRange.end {
		_ = ope.encrypt(plaintext)
		plaintext += int64(math.Pow(2, 24))
	}
}

func TestHugeOutputRange(t *testing.T) {
	inRange, _ := NewValueRange(0, 0)
	outRange, _ := NewValueRange(0, int64(math.Pow(2, 65)))
	cipher := NewOPE([]byte("key11"), inRange, outRange)
	result := cipher.encrypt(0)
	if result == 0 {
		t.Errorf("encrypt(0) expected!=0 for huge output range")
	}
}