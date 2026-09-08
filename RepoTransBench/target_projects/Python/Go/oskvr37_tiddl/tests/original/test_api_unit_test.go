package original

import (
	"testing"
)

type DummyAPI struct {
	CallCount int
	LastArg   int
}

func (api *DummyAPI) Add(a int, b int) int {
	api.CallCount++
	api.LastArg = a + b
	return a + b
}

func TestDummyAPIAdd(t *testing.T) {
	api := &DummyAPI{}
	result := api.Add(3, 4)
	if result != 7 {
		t.Errorf("Add(3,4) = %d, want 7", result)
	}
	if api.CallCount != 1 {
		t.Errorf("CallCount = %d, want 1", api.CallCount)
	}
	if api.LastArg != 7 {
		t.Errorf("LastArg = %d, want 7", api.LastArg)
	}
	result2 := api.Add(1, 1)
	if result2 != 2 {
		t.Errorf("Add(1,1) = %d, want 2", result2)
	}
	if api.CallCount != 2 {
		t.Errorf("CallCount after 2nd call = %d, want 2", api.CallCount)
	}
	if api.LastArg != 2 {
		t.Errorf("LastArg after 2nd call = %d, want 2", api.LastArg)
	}
}