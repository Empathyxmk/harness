package original

import (
	"testing"
)

type HmacHashFunction string

const (
	HmacSHA1   HmacHashFunction = "HmacSHA1"
	HmacSHA256 HmacHashFunction = "HmacSHA256"
	HmacSHA512 HmacHashFunction = "HmacSHA512"
)

type GoogleAuthenticatorConfig struct {
	WindowSize          int
	CodeDigits          int
	KeyRepresentation   KeyRepresentation
	TimeStepSizeInMillis int64
	HmacHashFunc        HmacHashFunction
	NumberOfScratchCodes int
	SecretBits          int
}

type GoogleAuthenticatorConfigBuilder struct {
	config GoogleAuthenticatorConfig
}

func NewGoogleAuthenticatorConfig() GoogleAuthenticatorConfig {
	return GoogleAuthenticatorConfig{
		WindowSize:            1,
		CodeDigits:            6,
		KeyRepresentation:     Base32,
		TimeStepSizeInMillis:  30000,
		HmacHashFunc:          HmacSHA1,
		NumberOfScratchCodes:  5,
		SecretBits:            80,
	}
}

func (b *GoogleAuthenticatorConfigBuilder) SetWindowSize(w int) *GoogleAuthenticatorConfigBuilder {
	b.config.WindowSize = w
	return b
}
func (b *GoogleAuthenticatorConfigBuilder) SetCodeDigits(d int) *GoogleAuthenticatorConfigBuilder {
	b.config.CodeDigits = d
	return b
}
func (b *GoogleAuthenticatorConfigBuilder) SetKeyRepresentation(r KeyRepresentation) *GoogleAuthenticatorConfigBuilder {
	b.config.KeyRepresentation = r
	return b
}
func (b *GoogleAuthenticatorConfigBuilder) SetTimeStepSizeInMillis(ms int64) *GoogleAuthenticatorConfigBuilder {
	b.config.TimeStepSizeInMillis = ms
	return b
}
func (b *GoogleAuthenticatorConfigBuilder) SetHmacHashFunction(f HmacHashFunction) *GoogleAuthenticatorConfigBuilder {
	b.config.HmacHashFunc = f
	return b
}
func (b *GoogleAuthenticatorConfigBuilder) SetNumberOfScratchCodes(n int) *GoogleAuthenticatorConfigBuilder {
	b.config.NumberOfScratchCodes = n
	return b
}
func (b *GoogleAuthenticatorConfigBuilder) SetSecretBits(s int) *GoogleAuthenticatorConfigBuilder {
	b.config.SecretBits = s
	return b
}

func (b *GoogleAuthenticatorConfigBuilder) Build() GoogleAuthenticatorConfig {
	return b.config
}

func TestDefaultConstructorAndGetters(t *testing.T) {
	config := NewGoogleAuthenticatorConfig()
	if config.WindowSize < 0 {
		t.Error("WindowSize should be >= 0")
	}
	if config.CodeDigits < 0 {
		t.Error("CodeDigits should be >= 0")
	}
	if config.KeyRepresentation == "" {
		t.Error("KeyRepresentation should not be empty")
	}
	if config.TimeStepSizeInMillis <= 0 {
		t.Error("TimeStepSizeInMillis should be > 0")
	}
	if config.HmacHashFunc == "" {
		t.Error("HmacHashFunc should not be empty")
	}
	if config.NumberOfScratchCodes < 0 {
		t.Error("NumberOfScratchCodes should be >= 0")
	}
	if config.SecretBits < 0 {
		t.Error("SecretBits should be >= 0")
	}
}

func TestBuilder(t *testing.T) {
	builder := &GoogleAuthenticatorConfigBuilder{}
	builder.SetWindowSize(4).
		SetCodeDigits(7).
		SetKeyRepresentation(Base64).
		SetTimeStepSizeInMillis(654321).
		SetHmacHashFunction(HmacSHA1).
		SetNumberOfScratchCodes(7).
		SetSecretBits(160)

	config := builder.Build()
	if config.WindowSize != 4 {
		t.Errorf("Expected 4, got %d", config.WindowSize)
	}
	if config.CodeDigits != 7 {
		t.Errorf("Expected 7, got %d", config.CodeDigits)
	}
	if config.KeyRepresentation != Base64 {
		t.Errorf("Expected BASE64, got %v", config.KeyRepresentation)
	}
	if config.TimeStepSizeInMillis != 654321 {
		t.Errorf("Expected 654321, got %d", config.TimeStepSizeInMillis)
	}
	if config.HmacHashFunc != HmacSHA1 {
		t.Errorf("Expected HmacSHA1, got %v", config.HmacHashFunc)
	}
	if config.NumberOfScratchCodes != 7 {
		t.Errorf("Expected 7, got %d", config.NumberOfScratchCodes)
	}
	if config.SecretBits != 160 {
		t.Errorf("Expected 160, got %d", config.SecretBits)
	}
}