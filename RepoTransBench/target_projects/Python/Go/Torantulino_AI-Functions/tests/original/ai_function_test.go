package original

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

// Test successful ai_function call with default model "gpt-4"
func TestAIFunctionSuccess(t *testing.T) {
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
				{Message: map[string]string{"content": "42"}},
			},
		}
	}

	result := aifunctions.AI_Function(
		"def add(a, b): return a + b",
		[]string{"2", "40"},
		"Adds two numbers",
	)
	if result != "42" {
		t.Errorf("Expected result '42', got '%s'", result)
	}
}

// Test ai_function with custom model argument
func TestAIFunctionCustomModel(t *testing.T) {
	prev := aifunctions.AIChatCompletionCreate
	defer func() { aifunctions.AIChatCompletionCreate = prev }()

	aifunctions.AIChatCompletionCreate = func(args map[string]interface{}) aifunctions.AIResponse {
		model, ok := args["model"].(string)
		if !ok || model != "gpt-3.5-turbo" {
			t.Fatalf("Expected model 'gpt-3.5-turbo', got: %v", args["model"])
		}
		return aifunctions.AIResponse{
			Choices: []aifunctions.AIChoice{
				{Message: map[string]string{"content": "7"}},
			},
		}
	}

	result := aifunctions.AI_Function(
		"def mul(a, b): return a * b",
		[]string{"3", "4"},
		"Multiply two numbers",
		"gpt-3.5-turbo",
	)
	if result != "7" {
		t.Errorf("Expected result '7', got '%s'", result)
	}
}

// Test ai_function handles no arguments correctly
func TestAIFunctionNoArgs(t *testing.T) {
	prev := aifunctions.AIChatCompletionCreate
	defer func() { aifunctions.AIChatCompletionCreate = prev }()

	aifunctions.AIChatCompletionCreate = func(args map[string]interface{}) aifunctions.AIResponse {
		return aifunctions.AIResponse{
			Choices: []aifunctions.AIChoice{
				{Message: map[string]string{"content": "no args"}},
			},
		}
	}

	result := aifunctions.AI_Function(
		"def f(): return None",
		[]string{},
		"No-argument function",
	)
	if result != "no args" {
		t.Errorf("Expected result 'no args', got '%s'", result)
	}
}

// Test the message construction logic of ai_function
func TestAIFunctionResponseStructure(t *testing.T) {
	prev := aifunctions.AIChatCompletionCreate
	defer func() { aifunctions.AIChatCompletionCreate = prev }()

	captured := make(map[string]interface{})
	aifunctions.AIChatCompletionCreate = func(args map[string]interface{}) aifunctions.AIResponse {
		captured["messages"] = args["messages"]
		return aifunctions.AIResponse{
			Choices: []aifunctions.AIChoice{
				{Message: map[string]string{"content": "X"}},
			},
		}
	}

	aifunctions.AI_Function("def f(x): return x", []string{"7"}, "Echo integer")

	msgSlice, ok := captured["messages"].([]map[string]string)
	if !ok {
		// Try converting []interface{} to []map[string]string
		tmp, ok2 := captured["messages"].([]interface{})
		if !ok2 || len(tmp) < 2 {
			t.Fatalf("messages not found or not a slice")
		}
		// Try to map types
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
	if userMsg["content"] != "7" {
		t.Errorf("User message content should be '7', got '%s'", userMsg["content"])
	}
}

// Helper
func contains(s, sub string) bool {
	return len(sub) == 0 || (len(s) >= len(sub) && (reflect.DeepEqual(s[0:len(sub)], sub) || contains(s[1:], sub)))
}