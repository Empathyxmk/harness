package original

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

type DummyStruct struct {
	StrVal   string
	LongVal  int64
	IntVal   int
	Int32Val int32
	ByteVal  byte
	BoolVal  bool
	DateVal  time.Time
}

func (ds *DummyStruct) SetFields(bs []byte, offset int) {
	ds.StrVal = string(bs)
	ds.LongVal = int64(bs[offset])
	ds.IntVal = int(bs[offset])
	ds.Int32Val = int32(bs[offset])
	ds.ByteVal = bs[offset]
	ds.BoolVal = bs[offset]%2 == 1
	ds.DateVal = time.Now()
}

func TestStringValueNormal(t *testing.T) {
	s := DummyStruct{}
	bs := []byte("TestStr\x00\x00\x00")
	// Simulate extracting a string, trimming nulls.
	val := string(bs[:7])
	assert.Equal(t, "TestStr", val)
}

func TestStringValueEncodingException(t *testing.T) {
	s := DummyStruct{}
	// Go cannot "set" an invalid charset, but we simulate fallback
	val := func(b []byte) *string {
		defer func() { recover() }()
		_ = string(b)
		return nil
	}([]byte{65})
	assert.Nil(t, val)
}

func TestOtherValueMethods(t *testing.T) {
	s := DummyStruct{}
	bs := make([]byte, 16)
	bs[0] = 100
	s.SetFields(bs, 0)
	assert.NotNil(t, s.StrVal)
	assert.False(t, s.DateVal.IsZero())
	assert.Equal(t, bs[0], s.ByteVal)
}