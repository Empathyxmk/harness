package original

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

func TestGetFromDictOrEnvEmptyDictNoEnv(t *testing.T) {
	key := "TEST_MISSING_KEY"
	origVal, hasOrig := os.LookupEnv(key)
	os.Unsetenv(key)
	defer func() {
		if hasOrig {
			os.Setenv(key, origVal)
		} else {
			os.Unsetenv(key)
		}
	}()
	_, err := betterprompt.GetFromDictOrEnv(key, map[string]string{})
	if err == nil {
		t.Fatalf("Expected ValueError for missing key '%s', got nil", key)
	}
	if !contains(err.Error(), key) {
		t.Errorf("Expected key in error message, got: %v", err)
	}
}

func TestGetFromDictOrEnvNoneDictEnv(t *testing.T) {
	key := "ENV_ONLY_KEY"
	origVal, hasOrig := os.LookupEnv(key)
	os.Setenv(key, "val")
	defer func() {
		if hasOrig {
			os.Setenv(key, origVal)
		} else {
			os.Unsetenv(key)
		}
	}()
	val, err := betterprompt.GetFromDictOrEnv(key, nil)
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if val != "val" {
		t.Errorf("Expected 'val', got: %v", val)
	}
}

func TestGetFromDictOrEnvDictEmpty(t *testing.T) {
	key := "NO_DICT_KEY"
	origVal, hasOrig := os.LookupEnv(key)
	os.Setenv(key, "from_env")
	defer func() {
		if hasOrig {
			os.Setenv(key, origVal)
		} else {
			os.Unsetenv(key)
		}
	}()
	val, err := betterprompt.GetFromDictOrEnv(key, map[string]string{})
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if val != "from_env" {
		t.Errorf("Expected 'from_env', got: %v", val)
	}
}

func TestOpenAIClassAndDummy(t *testing.T) {
	result := betterprompt.OpenAICompletionCreate()
	if result == nil {
		t.Error("Expected result map, got nil")
	}
	if _, ok := result["choices"]; !ok {
		t.Errorf("Result should contain 'choices', got: %v", result)
	}
}

func TestCallOpenAIAPIKey(t *testing.T) {
	dummyLogprobs := []float64{0.4, 0.5, 0.6}
	betterprompt.MockOpenAICompletion(dummyLogprobs)
	result, err := betterprompt.CallOpenAI("prompt", "explicit_key", "")
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if !equalFloatSlice(result, dummyLogprobs) {
		t.Errorf("Expected %v, got %v", dummyLogprobs, result)
	}
}

func TestCalculatePerplexityRegularEdge(t *testing.T) {
	tokenLogprobs := []float64{0, -1, -2}
	perplexity := betterprompt.CalculatePerplexity(tokenLogprobs)
	expected := math.Exp(-sum(tokenLogprobs) / float64(len(tokenLogprobs)))
	if math.Abs(perplexity-expected) > 1e-8 {
		t.Errorf("Expected %v, got %v", expected, perplexity)
	}
}

func TestCalculatePerplexityEmptyEdge(t *testing.T) {
	result := betterprompt.CalculatePerplexity([]float64{})
	if !math.IsInf(result, 1) && !math.IsInf(result, -1) {
		t.Errorf("Expected Inf for empty input, got: %v", result)
	}
}