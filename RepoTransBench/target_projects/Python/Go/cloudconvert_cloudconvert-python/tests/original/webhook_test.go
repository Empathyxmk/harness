package original

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"testing"
)

type Webhook struct{}

func (w *Webhook) Verify(payload, sig, secret string) bool {
	h := hmac.New(sha256.New, []byte(secret))
	h.Write([]byte(payload))
	expectedSig := hex.EncodeToString(h.Sum(nil))
	return expectedSig == sig
}

func TestWebhookValidSignature(t *testing.T) {
	payload := "data"
	secret := "secret"
	h := hmac.New(sha256.New, []byte(secret))
	h.Write([]byte(payload))
	expectedSig := hex.EncodeToString(h.Sum(nil))
	w := &Webhook{}
	if !w.Verify(payload, expectedSig, secret) {
		t.Errorf("Expected valid signature to verify")
	}
}

func TestWebhookInvalidSignature(t *testing.T) {
	payload := "data"
	secret := "secret"
	wrongSig := "abc"
	w := &Webhook{}
	if w.Verify(payload, wrongSig, secret) {
		t.Errorf("Wrong signature should not verify")
	}
}

func TestWebhookEmptyPayload(t *testing.T) {
	payload := ""
	secret := "secret"
	h := hmac.New(sha256.New, []byte(secret))
	h.Write([]byte(payload))
	expectedSig := hex.EncodeToString(h.Sum(nil))
	w := &Webhook{}
	if !w.Verify(payload, expectedSig, secret) {
		t.Errorf("Empty payload signature did not verify")
	}
}

func TestWebhookWrongSecret(t *testing.T) {
	payload := "data"
	secret := "right"
	wrongSecret := "wrong"
	h := hmac.New(sha256.New, []byte(secret))
	h.Write([]byte(payload))
	correctSig := hex.EncodeToString(h.Sum(nil))
	w := &Webhook{}
	if w.Verify(payload, correctSig, wrongSecret) {
		t.Errorf("Signature verified with wrong secret, expected false")
	}
}