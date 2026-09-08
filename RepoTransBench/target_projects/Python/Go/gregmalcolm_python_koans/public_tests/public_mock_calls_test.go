package public_tests

import (
	"testing"
)

func TestPublicMultipleCalls(t *testing.T) {
	m := &PublicMock{}
	m.Call(11)
	m.Call(22)
	if m.callCount != 2 {
		t.Errorf("call_count: expected 2, got %d", m.callCount)
	}
	if len(m.callArgsList) < 2 || m.callArgsList[0][0] != 11 || m.callArgsList[1][0] != 22 {
		t.Error("callArgsList not correct")
	}
}

func TestPublicAssertCalledWith(t *testing.T) {
	m := &PublicMock{}
	m.Call(999, 888)
	ok := false
	args := m.callArgs
	if len(args) == 2 && args[0] == 999 && args[1] == 888 {
		ok = true
	}
	if !ok {
		t.Error("assert_called_with failed")
	}
}