package public_tests

import (
	"math"
	"os"
	"testing"

	"betterprompt"
)

func contains(hay, needle string) bool {
	return len(hay) >= len(needle) && (needle == hay || contains(hay[1:], needle))
}
func equalFloatSlice(a, b []float64) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if math.Abs(a[i]-b[i]) > 1e-9 {
			return false
		}
	}
	return true
}
func sum(arr []float64) float64 {
	s := 0.0
	for _, v := range arr {
		s += v
	}
	return s
}

// --- env helpers
func setEnv(key, val string) (orig string, present bool) {
	orig, present = os.LookupEnv(key)
	os.Setenv(key, val)
	return
}
func unsetEnv(key string) (orig string, present bool) {
	orig, present = os.LookupEnv(key)
	os.Unsetenv(key)
	return
}

func TestPublicGetFromDictOrEnvMissing(t *testing.T) {
	key := "PUBLIC_ENV_KEY"
	orig, present := unsetEnv(key)
	defer func() {
		if present {
			os.Setenv(key, orig)
		} else {
			os.Unsetenv(key)
		}
	}()

	_, err := betterprompt.GetFromDictOrEnv(key, map[string]string{})
	if err == nil {
		t.Fatalf("Expected error for missing key '%s', got nil", key)
	}
	if !contains(err.Error(), key) {
		t.Errorf("Expected key in error, got %v", err)
	}
}

func TestPublicGetFromDictOrEnvDict(t *testing.T) {
	key := "DICT_ONLY_KEY"
	d := map[string]string{key: "dict_value"}
	orig, present := setEnv(key, "env_value")
	defer func() {
		if present {
			os.Setenv(key, orig)
		} else {
			os.Unsetenv(key)
		}
	}()
	val, err := betterprompt.GetFromDictOrEnv(key, d)
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if val != "dict_value" {
		t.Errorf("Expected 'dict_value', got: %v", val)
	}
}

func TestPublicGetFromDictOrEnvEnv(t *testing.T) {
	key := "ENV_ONLY_KEY_PUBLIC"
	orig, present := unsetEnv(key)
	setEnv(key, "from_env_public")
	defer func() {
		if present {
			os.Setenv(key, orig)
		} else {
			os.Unsetenv(key)
		}
	}()
	val, err := betterprompt.GetFromDictOrEnv(key, nil)
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if val != "from_env_public" {
		t.Errorf("Expected 'from_env_public', got: %v", val)
	}
}

func TestPublicOpenAIClassDummy(t *testing.T) {
	result := betterprompt.OpenAICompletionCreate()
	if result == nil {
		t.Error("Expected result map, got nil")
	}
	if _, ok := result["choices"]; !ok {
		t.Error("'choices' missing in dummy openai completion result")
	}
}

func TestPublicCallOpenAIAPIKey(t *testing.T) {
	dummyLogprobs := []float64{1.23, -0.8, 3.14}
	betterprompt.MockOpenAICompletion(dummyLogprobs)
	result, err := betterprompt.CallOpenAI("test prompt", "a_public_key", "")
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if !equalFloatSlice(result, dummyLogprobs) {
		t.Errorf("Expected %v, got %v", dummyLogprobs, result)
	}
}

func TestPublicCalculatePerplexityAllNegative(t *testing.T) {
	tokenLogprobs := []float64{-2, -4, -6}
	expected := math.Exp(-sum(tokenLogprobs) / float64(len(tokenLogprobs)))
	perplexity := betterprompt.CalculatePerplexity(tokenLogprobs)
	if math.Abs(perplexity-expected) > 1e-8 {
		t.Errorf("Expected %v, got %v", expected, perplexity)
	}
}

func TestPublicCalculatePerplexityEmpty(t *testing.T) {
	result := betterprompt.CalculatePerplexity([]float64{})
	if !math.IsInf(result, 1) && !math.IsInf(result, -1) {
		t.Errorf("Expected Inf for empty input, got: %v", result)
	}
}