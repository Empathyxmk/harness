package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
	. "pallets_itsdangerous/src/itsdangerous/exc"
)

func TestBadSignatureStrPublic(t *testing.T) {
	sig := NewBadSignature("Diff reason", "")
	assert.Contains(t, sig.Error(), "Diff reason")
}

func TestBadPayloadStrPublic(t *testing.T) {
	bp := NewBadPayload("Different", nil)
	assert.Contains(t, bp.Error(), "Different")
}

func TestBadTimeSignatureStrPublic(t *testing.T) {
	bts := NewBadTimeSignature("ReasonZZZ", "", nil)
	assert.Contains(t, bts.Error(), "ReasonZZZ")
}

func TestSignatureExpiredStrPublic(t *testing.T) {
	se := NewSignatureExpired("Late!", "", nil)
	assert.Contains(t, se.Error(), "Late!")
}