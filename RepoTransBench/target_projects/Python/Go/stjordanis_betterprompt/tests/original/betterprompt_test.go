package original

import (
	"math"
	"testing"

	"betterprompt"
)

func hasInSlice(slice []string, s string) bool {
	for _, el := range slice {
		if el == s {
			return true
		}
	}
	return false
}

func TestMetadata(t *testing.T) {
	if _, ok := betterprompt.Version().(string); !ok {
		t.Error("Version is not a string")
	}
	if _, ok := betterprompt.Author().(string); !ok {
		t.Error("Author is not a string")
	}
	if _, ok := betterprompt.Copyright().(string); !ok {
		t.Error("Copyright is not a string")
	}
	if _, ok := betterprompt.License().(string); !ok {
		t.Error("License is not a string")
	}
	if !hasInSlice(betterprompt.All(), "get_from_dict_or_env") {
		t.Error("'get_from_dict_or_env' not in __all__")
	}
}

func TestDummyOpenAICompletionCreate(t *testing.T) {
	res := betterprompt.OpenAICompletionCreate()
	if res == nil {
		t.Error("Expected result map, got nil")
	}
	if _, ok := res["choices"]; !ok {
		t.Error("'choices' not in dummy openai completion result")
	}
}

func TestOpenAICompletionStatic(t *testing.T) {
	dummyLogprobs := []float64{0.5}
	betterprompt.MockOpenAICompletion(dummyLogprobs)
	res := betterprompt.OpenAICompletionCreate()
	choices, ok := res["choices"].([]map[string]interface{})
	if !ok || len(choices) == 0 {
		t.Fatal("choices missing or invalid")
	}
	logprobs, ok := choices[0]["logprobs"].(map[string]interface{})
	if !ok {
		t.Fatal("logprobs missing or invalid")
	}
	tokenLogprobs, ok := logprobs["token_logprobs"].([]float64)
	if !ok || len(tokenLogprobs) != 1 || math.Abs(tokenLogprobs[0]-0.5) > 1e-8 {
		t.Fatalf("Expected logprobs [0.5], got %v", tokenLogprobs)
	}
}