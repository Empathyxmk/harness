package original

import (
	"errors"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	. "pallets_itsdangerous/src/itsdangerous/exc"
)

func TestBadDataStrAndMessage(t *testing.T) {
	err := NewBadData("msg-1")
	assert.Equal(t, "msg-1", err.Error())
	assert.Equal(t, "msg-1", err.Message())
}

func TestBadSignaturePayload(t *testing.T) {
	err := NewBadSignature("fail sig", "abc")
	assert.Equal(t, "fail sig", err.Error())
	assert.Equal(t, "abc", err.Payload())
}

func TestBadTimeSignaturePayloadAndDate(t *testing.T) {
	dt := time.Now()
	err := NewBadTimeSignature("fail time sig", "bbb", dt)
	assert.Equal(t, "fail time sig", err.Message())
	assert.Equal(t, "bbb", err.Payload())
	assert.Equal(t, dt, err.DateSigned())
}

func TestSignatureExpiredIsSubclass(t *testing.T) {
	var e error = &SignatureExpired{}
	_, ok := e.(*BadTimeSignature)
	assert.True(t, ok)
}

func TestBadHeaderPayloadAndError(t *testing.T) {
	origEx := errors.New("boom")
	bh := NewBadHeader("bad head", "yy", map[string]string{"x": "y"}, origEx)
	assert.Equal(t, "bad head", bh.Message())
	assert.Equal(t, "yy", bh.Payload())
	assert.Equal(t, map[string]string{"x": "y"}, bh.Header())
	assert.Equal(t, origEx, bh.OriginalError())
}

func TestBadPayloadOriginalError(t *testing.T) {
	origEx := errors.New("failz")
	bp := NewBadPayload("bad pay", origEx)
	assert.Equal(t, "bad pay", bp.Message())
	assert.Equal(t, origEx, bp.OriginalError())
}