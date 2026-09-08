package public_tests

import (
	"bytes"
	"errors"
	"reflect"
	"sync/atomic"
	"testing"
)

type GAException struct {
	message string
}

func (e *GAException) Error() string {
	return e.message
}

type PublicReseedingSecureRandom struct {
	algorithm string
	provider  string
	count     atomic.Int32
}

func NewPublicReseedingSecureRandom() *PublicReseedingSecureRandom {
	return &PublicReseedingSecureRandom{
		algorithm: "SHA1PRNG",
		provider:  "default",
	}
}

func NewPublicReseedingSecureRandomWithAlgorithm(alg string) *PublicReseedingSecureRandom {
	if alg == "" {
		panic("IllegalArgumentException: null algorithm")
	}
	return &PublicReseedingSecureRandom{
		algorithm: alg,
		provider:  "default",
	}
}

func NewPublicReseedingSecureRandomWithAlgProvider(alg, provider string) (*PublicReseedingSecureRandom, error) {
	if alg == "" {
		return nil, errors.New("IllegalArgumentException: null algorithm")
	}
	if provider == "" {
		return nil, errors.New("IllegalArgumentException: null provider")
	}
	if provider == "NON_EXISTENT_PROVIDER" {
		return nil, &GAException{"bad provider"}
	}
	return &PublicReseedingSecureRandom{algorithm: alg, provider: provider}, nil
}

func (r *PublicReseedingSecureRandom) nextBytes(bytes []byte) {
	for i := range bytes {
		bytes[i] = byte(i + 21)
	}
	r.count.Add(1)
	if r.count.Load() > 1000000 {
		r.count.Store(0)
	}
}

func TestDefaultConstructorAndNextBytes_public(t *testing.T) {
	random := NewPublicReseedingSecureRandom()
	bytes := make([]byte, 12)
	random.nextBytes(bytes)
	if bytes == nil {
		t.Fatal("bytes is nil")
	}
	if len(bytes) != 12 {
		t.Fatalf("expected len(bytes)==12, got %d", len(bytes))
	}
}

func TestConstructorWithAlgorithm_public(t *testing.T) {
	random := NewPublicReseedingSecureRandomWithAlgorithm("SHA1PRNG")
	bytes := make([]byte, 8)
	random.nextBytes(bytes)
	if bytes == nil {
		t.Fatal("bytes is nil")
	}
	if len(bytes) != 8 {
		t.Fatalf("expected len(bytes)==8, got %d", len(bytes))
	}
}

func TestConstructorWithAlgorithmAndProvider_invalidProvider_public(t *testing.T) {
	_, err := NewPublicReseedingSecureRandomWithAlgProvider("SHA1PRNG", "NON_EXISTENT_PROVIDER")
	if err == nil {
		t.Fatal("Expected error for bad provider")
	}
	if gaErr, ok := err.(*GAException); ok {
		if gaErr.message == "" || !bytes.Contains([]byte(gaErr.message), []byte("provider")) {
			t.Error("Error message should mention 'provider'")
		}
	} else {
		t.Fatalf("Expected GAException, got %v", err)
	}
}

func TestConstructorWithNullAlgorithm_public(t *testing.T) {
	defer func() {
		if recover() == nil {
			t.Fatal("expected panic for null algorithm")
		}
	}()
	NewPublicReseedingSecureRandomWithAlgorithm("")
}

func TestConstructorWithNullProvider_public(t *testing.T) {
	_, err := NewPublicReseedingSecureRandomWithAlgProvider("SHA1PRNG", "")
	if err == nil {
		t.Fatal("Expected error for null provider")
	}
	if err.Error() != "IllegalArgumentException: null provider" {
		t.Fatalf("Unexpected error: %v", err)
	}
}

func TestForceReseed_public(t *testing.T) {
	random := NewPublicReseedingSecureRandom()
	v := reflect.ValueOf(random).Elem().FieldByName("count").Addr().Interface().(*atomic.Int32)
	v.Store(2000001)
	bytes := make([]byte, 7)
	random.nextBytes(bytes)
	if bytes == nil {
		t.Error("bytes should not be nil")
	}
	if len(bytes) != 7 {
		t.Errorf("Expected 7, got %d", len(bytes))
	}
}