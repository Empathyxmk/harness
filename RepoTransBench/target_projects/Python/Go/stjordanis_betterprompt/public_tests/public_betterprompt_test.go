package public_tests

import (
	"math"
	"os"
	"testing"

	"betterprompt"
)

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

func setEnv(key, val string) (orig string, present bool) {
	orig, present = os.LookupEnv(key)
	os.Setenv(key, val)
	return
}

func TestPublicCallOpenAICustomModel(t *testing.T) {
	dummyLogprobs := []float64{-0.1, 2.5, -4.3}
	betterprompt.MockOpenAICompletionWithModel(dummyLogprobs, "public-model")
	res, err := betterprompt.CallOpenAI("sample prompt here", "anypublickey", "public-model")
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if !equalFloatSlice(res, dummyLogprobs) {
		t.Errorf("Expected %v, got %v", dummyLogprobs, res)
	}
}

func TestPublicCallOpenAIEnv(t *testing.T) {
	dummyLogprobs := []float64{7, 8}
	betterprompt.MockOpenAICompletion(dummyLogprobs)

	orig, present := setEnv("OPENAI_API_KEY", "public_env_key_test")
	defer func() {
		if present {
			os.Setenv("OPENAI_API_KEY", orig)
		} else {
			os.Unsetenv("OPENAI_API_KEY")
		}
	}()

	res, err := betterprompt.CallOpenAI("prompt string", "", "")
	if err != nil {
		t.Errorf("Unexpected error: %v", err)
	}
	if !equalFloatSlice(res, dummyLogprobs) {
		t.Errorf("Expected %v, got %v", dummyLogprobs, res)
	}
}

func TestPublicCalculatePerplexityDifferent(t *testing.T) {
	tokenLogprobs := []float64{-1, 0, 1, 2}
	expect := math.Exp(-sum(tokenLogprobs) / float64(len(tokenLogprobs)))
	actual := betterprompt.CalculatePerplexity(tokenLogprobs)
	if math.Abs(actual-expect) > 1e-8 {
		t.Errorf("Expected %v, got %v", expect, actual)
	}
}