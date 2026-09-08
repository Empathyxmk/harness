package public_tests

import (
	"reflect"
	"testing"

	aifunctions "torantulino_ai_functions"
)

// DummyChoice and DummyResponse simulates OpenAI response objects using Go structs.
type DummyChoice struct {
	Message map[string]string
}

type DummyResponse struct {
	Choices []DummyChoice
}

// Public test: ai_function success case
func TestPublicAIFunctionSuccess(t *testing.T) {
	prev := aifunctions.AIChatCompletionCreate
	defer func() { aifunctions.AIChatCompletionCreate = prev }()

	aifunctions.AIChatCompletionCreate = func(args map[string]interface{}) aifunctions.AIResponse {
		model, ok := args["model"].(string)
		if !ok || model != "gpt-4" {
			t.Fatalf("Expected model 'gpt-4', got: %v", args["model"])
		}
		if _, ok := args["messages"]; !ok {
			t.Fatalf("'messages' not found in args")
		}
		return aifunctions.AIResponse{
			Choices: []aifunctions.AIChoice{
				{Message: map[string]string{"content": "17"}},
			},
		}
	}

	result := aifunctions.AI_Function(
		"def subtract(a, b): return a - b",
		[]string{"20", "3"},
		"Subtracts two numbers",
	)
	if result != "17" {
		t.Errorf("Expected result '17', got '%s'", result)
	}
}

// Public test: ai_function custom model
func TestPublicAIFunctionCustomModel(t *testing.T) {
	prev := aifunctions.AIChatCompletionCreate
	defer func() { aifunctions.AIChatCompletionCreate = prev }()

	aifunctions.AIChatCompletionCreate = func(args map[string]interface{}) aifunctions.AIResponse {
		model, ok := args["model"].(string)
		if !ok || model != "gpt-3.5-turbo" {
			t.Fatalf("Expected model 'gpt-3.5-turbo', got: %v", args["model"])
		}
		return aifunctions.AIResponse{
			Choices: []aifunctions.AIChoice{
				{Message: map[string]string{"content": "15"}},
			},
		}
	}

	result := aifunctions.AI_Function(
		"def div(a, b): return a // b",
		[]string{"30", "2"},
		"Divide and floor two numbers",
		"gpt-3.5-turbo",
	)
	if result != "15" {
		t.Errorf("Expected result '15', got '%s'", result)
	}
}

// Public test: ai_function with no args
func TestPublicAIFunctionNoArgs(t *testing.T) {
	prev := aifunctions.AIChatCompletionCreate
	defer func() { aifunctions.AIChatCompletionCreate = prev }()

	aifunctions.AIChatCompletionCreate = func(args map[string]interface{}) aifunctions.AIResponse {
		return aifunctions.AIResponse{
			Choices: []aifunctions.AIChoice{
				{Message: map[string]string{"content": "empty args handled"}},
			},
		}
	}

	result := aifunctions.AI_Function(
		"def hello(): return 'hello'",
		[]string{},
		"No-argument greeting function",
	)
	if result != "empty args handled" {
		t.Errorf("Expected result 'empty args handled', got '%s'", result)
	}
}

// Public test: check message building logic with new data.
func TestPublicAIFunctionResponseStructure(t *testing.T) {
	prev := aifunctions.AIChatCompletionCreate
	defer func() { aifunctions.AIChatCompletionCreate = prev }()

	captured := make(map[string]interface{})
	aifunctions.AIChatCompletionCreate = func(args map[string]interface{}) aifunctions.AIResponse {
		captured["messages"] = args["messages"]
		return aifunctions.AIResponse{
			Choices: []aifunctions.AIChoice{
				{Message: map[string]string{"content": "Y"}},
			},
		}
	}

	aifunctions.AI_Function("def echo(s): return s", []string{"foo"}, "Echo string argument")

	msgSlice, ok := captured["messages"].([]map[string]string)
	if !ok {
		// Try converting []interface{} to []map[string]string
		tmp, ok2 := captured["messages"].([]interface{})
		if !ok2 || len(tmp) < 2 {
			t.Fatalf("messages not found or not a slice")
		}
		msgSlice = []map[string]string{}
		for _, v := range tmp {
			if mm, ok := v.(map[string]string); ok {
				msgSlice = append(msgSlice, mm)
			} else if mmRaw, ok := v.(map[string]interface{}); ok {
				ms := make(map[string]string)
				for k, val := range mmRaw {
					if sval, ok := val.(string); ok {
						ms[k] = sval
					}
				}
				msgSlice = append(msgSlice, ms)
			}
		}
	}

	if len(msgSlice) < 2 {
		t.Fatalf("Less than two messages in slice: %v", msgSlice)
	}

	sysMsg := msgSlice[0]
	if sysMsg["role"] != "system" {
		t.Errorf("System message role wrong, got '%s'", sysMsg["role"])
	}
	if sysMsg["content"] == "" || !contains(sysMsg["content"], "python function") {
		t.Errorf("System message content should mention 'python function', got '%s'", sysMsg["content"])
	}
	userMsg := msgSlice[1]
	if userMsg["role"] != "user" {
		t.Errorf("User message role wrong, got '%s'", userMsg["role"])
	}
	if userMsg["content"] != "foo" {
		t.Errorf("User message content should be 'foo', got '%s'", userMsg["content"])
	}
}

// Helper
func contains(s, sub string) bool {
	return len(sub) == 0 || (len(s) >= len(sub) && (reflect.DeepEqual(s[0:len(sub)], sub) || contains(s[1:], sub)))
}