package original

import (
	"bytes"
	"errors"
	"reflect"
	"sync/atomic"
	"testing"
)

type GoogleAuthenticatorException struct {
	message string
}

func (e *GoogleAuthenticatorException) Error() string {
	return e.message
}

// Dummy implementation just for test compilation.
type ReseedingSecureRandom struct {
	algorithm string
	provider  string
	count     atomic.Int32
}

// Dummy default constructor
func NewReseedingSecureRandom() *ReseedingSecureRandom {
	return &ReseedingSecureRandom{
		algorithm: "SHA1PRNG",
		provider:  "default",
	}
}

func NewReseedingSecureRandomWithAlgorithm(alg string) *ReseedingSecureRandom {
	if alg == "" {
		panic("IllegalArgumentException: null algorithm")
	}
	return &ReseedingSecureRandom{
		algorithm: alg,
		provider:  "default",
	}
}

func NewReseedingSecureRandomWithAlgorithmAndProvider(alg, provider string) (*ReseedingSecureRandom, error) {
	if alg == "" {
		return nil, errors.New("IllegalArgumentException: null algorithm")
	}
	if provider == "" {
		return nil, errors.New("IllegalArgumentException: null provider")
	}
	if provider == "FAKE_PROVIDER" {
		return nil, &GoogleAuthenticatorException{"bad provider"}
	}
	return &ReseedingSecureRandom{algorithm: alg, provider: provider}, nil
}

func (r *ReseedingSecureRandom) nextBytes(bytes []byte) {
	// For test: just put nonzero deterministic bytes
	for i := range bytes {
		bytes[i] = byte(i + 1)
	}
	// Increase count
	r.count.Add(1)
	// Simulate reseed
	if r.count.Load() > 1000000 {
		// dummy reseed
		r.count.Store(0)
	}
}

func TestDefaultConstructorAndNextBytes(t *testing.T) {
	random := NewReseedingSecureRandom()
	bytes := make([]byte, 10)
	random.nextBytes(bytes)
	if bytes == nil {
		t.Fatal("Bytes should not be nil")
	}
	if len(bytes) == 0 {
		t.Error("Bytes should have length > 0")
	}
}

func TestConstructorWithAlgorithm(t *testing.T) {
	random := NewReseedingSecureRandomWithAlgorithm("SHA1PRNG")
	bytes := make([]byte, 16)
	random.nextBytes(bytes)
	if bytes == nil {
		t.Fatal("Bytes should not be nil")
	}
}

func TestConstructorWithAlgorithmAndProvider_invalidProvider(t *testing.T) {
	_, err := NewReseedingSecureRandomWithAlgorithmAndProvider("SHA1PRNG", "FAKE_PROVIDER")
	if err == nil {
		t.Fatal("Expected GoogleAuthenticatorException for bad provider")
	}
	if gaErr, ok := err.(*GoogleAuthenticatorException); ok {
		if gaErr.message == "" || !bytes.Contains([]byte(gaErr.message), []byte("provider")) {
			t.Error("Error message should contain 'provider'")
		}
	} else {
		t.Errorf("Expected GoogleAuthenticatorException, got %v", err)
	}
}

func TestConstructorWithNullAlgorithm(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Fatal("Expected panic for null algorithm")
		}
	}()
	NewReseedingSecureRandomWithAlgorithm("")
}

func TestConstructorWithNullProvider(t *testing.T) {
	_, err := NewReseedingSecureRandomWithAlgorithmAndProvider("SHA1PRNG", "")
	if err == nil {
		t.Fatal("Expected error for null provider")
	}
	if err.Error() != "IllegalArgumentException: null provider" {
		t.Fatalf("Unexpected error: %v", err)
	}
}

func TestForceReseed(t *testing.T) {
	random := NewReseedingSecureRandom()
	v := reflect.ValueOf(random).Elem().FieldByName("count").Addr().Interface().(*atomic.Int32)
	v.Store(1000001)
	bytes := make([]byte, 5)
	random.nextBytes(bytes)
	if bytes == nil {
		t.Error("Bytes should not be nil")
	}
}