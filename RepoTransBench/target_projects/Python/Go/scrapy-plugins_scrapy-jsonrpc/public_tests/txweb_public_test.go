package public_tests

import (
	"fmt"
	"testing"
)

// Dummy Error, Handler, NOT_FOUND implementation for test port

type Error struct {
	Code    int
	Message string
	Data    map[string]interface{}
}

func (e Error) Error() string         { return e.Message }
func (e Error) String() string        { return fmt.Sprintf("Error(%d, '%s')", e.Code, e.Message) }
func (e Error) DataField() interface{} { return e.Data }

var NOT_FOUND = Error{404, "Not Found", nil}

type Handler struct{}

func (h Handler) Call(args ...interface{}) error { return NOT_FOUND }

func TestPublicErrorProperties(t *testing.T) {
	err := Error{1000, "unknown error", map[string]interface{}{"prop": "value"}}
	if err.Code != 1000 {
		t.Errorf("Code mismatch: %v", err.Code)
	}
	if err.Message != "unknown error" {
		t.Errorf("Message mismatch: %v", err.Message)
	}
	if !reflectDeepEqualMap(err.Data, map[string]interface{}{"prop": "value"}) {
		t.Errorf("Data field mismatch: %v", err.Data)
	}
}

func reflectDeepEqualMap(a, b map[string]interface{}) bool {
	if a == nil && b == nil {
		return true
	}
	if a == nil || b == nil {
		return false
	}
	if len(a) != len(b) {
		return false
	}
	for k, v := range a {
		if b[k] != v {
			return false
		}
	}
	return true
}

func TestPublicErrorStrRepr(t *testing.T) {
	err := Error{404, "resource not here", nil}
	if err.Error() != "resource not here" {
		t.Errorf("Error string wrong: %v", err.Error())
	}
	if err.String() != "Error(404, 'resource not here')" {
		t.Errorf("Error string wrong: %v", err.String())
	}
}

func TestPublicHandlerReturnsNotFound(t *testing.T) {
	handler := Handler{}
	err := handler.Call()
	if err != NOT_FOUND {
		t.Errorf("Handler did not return NOT_FOUND: %+v", err)
	}
	if err.Code != 404 {
		t.Errorf("Error code must be 404 got %v", err.Code)
	}
	if err.Message != "Not Found" {
		t.Errorf("Error message wrong: %v", err.Message)
	}
}