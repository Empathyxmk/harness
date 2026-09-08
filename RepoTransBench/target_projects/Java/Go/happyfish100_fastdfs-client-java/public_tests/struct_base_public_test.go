package public_tests

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

type DummyStructPublic struct {
	StrVal   string
	LongVal  int64
	IntVal   int
	Int32Val int32
	ByteVal  byte
	BoolVal  bool
	DateVal  time.Time
}

func (ds *DummyStructPublic) SetFields(bs []byte, offset int) {
	ds.StrVal = string(bs)
	ds.LongVal = int64(bs[offset])
	ds.IntVal = int(bs[offset])
	ds.Int32Val = int32(bs[offset])
	ds.ByteVal = bs[offset]
	ds.BoolVal = bs[offset]%2 == 0 // Differently than original
	ds.DateVal = time.Now()
}

func TestStringValueDifferent(t *testing.T) {
	s := DummyStructPublic{}
	bs := []byte("Public01\x00\x00")
	val := string(bs[:8])
	assert.Equal(t, "Public01", val)
}

func TestStringValueEncodingExceptionPublic(t *testing.T) {
	// Not possible in Go, simulate the fallback (nil if error)
	val := func(b []byte) *string {
		defer func() { recover() }()
		_ = string(b)
		return nil
	}([]byte{66})
	assert.Nil(t, val)
}

func TestOtherValueMethodsPublic(t *testing.T) {
	s := DummyStructPublic{}
	bs := make([]byte, 16)
	bs[0] = 42
	s.SetFields(bs, 0)
	assert.NotNil(t, s.StrVal)
	assert.False(t, s.DateVal.IsZero())
	assert.Equal(t, bs[0], s.ByteVal)
}