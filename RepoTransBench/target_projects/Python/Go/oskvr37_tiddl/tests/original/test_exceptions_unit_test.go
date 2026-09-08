package original

import (
	"fmt"
	"testing"
)

type ApiError struct {
	Status      int
	SubStatus   int
	UserMessage string
	ErrorCode   int
	Message     string
	OtherFields map[string]interface{}
}

func (e *ApiError) Error() string {
	return fmt.Sprintf("ApiError: %d %s", e.Status, e.UserMessage)
}

func (e *ApiError) String() string {
	return fmt.Sprintf("ApiError(status=%d, subStatus=%d, userMessage=%s, errorCode=%d, message=%s, others=%v)",
		e.Status, e.SubStatus, e.UserMessage, e.ErrorCode, e.Message, e.OtherFields)
}

func NewApiError(fields map[string]interface{}) *ApiError {
	ae := &ApiError{
		OtherFields: map[string]interface{}{},
	}
	// extract known fields
	if v, ok := fields["status"]; ok {
		ae.Status = toInt(v)
	}
	if v, ok := fields["subStatus"]; ok {
		ae.SubStatus = toInt(v)
	}
	if v, ok := fields["userMessage"]; ok {
		if v != nil {
			ae.UserMessage = fmt.Sprintf("%v", v)
		} else {
			ae.UserMessage = ""
		}
	}
	if v, ok := fields["errorCode"]; ok {
		ae.ErrorCode = toInt(v)
	}
	if v, ok := fields["message"]; ok {
		ae.Message = fmt.Sprintf("%v", v)
	}
	// any other fields
	for k, v := range fields {
		if k != "status" && k != "subStatus" && k != "userMessage" && k != "errorCode" && k != "message" {
			ae.OtherFields[k] = v
		}
	}
	return ae
}

func toInt(x interface{}) int {
	switch v := x.(type) {
	case int:
		return v
	case int32:
		return int(v)
	case int64:
		return int(v)
	case float64:
		return int(v)
	case float32:
		return int(v)
	case string:
		var i int
		fmt.Sscanf(v, "%d", &i)
		return i
	default:
		return 0
	}
}

func TestApiErrorStrReprFields(t *testing.T) {
	err := NewApiError(map[string]interface{}{
		"status":      404,
		"subStatus":   0,
		"userMessage": "not found",
		"errorCode":   999,
		"message":     "msg",
	})
	if got := err.Error(); !contains(got, "404") {
		t.Errorf("err.Error() = %q, want contains %q", got, "404")
	}
	if got := err.String(); !contains(got, "not found") {
		t.Errorf("err.String() = %q, want contains %q", got, "not found")
	}
	if err.Status != 404 {
		t.Errorf("Status = %d, want 404", err.Status)
	}
	if err.ErrorCode != 999 {
		t.Errorf("ErrorCode = %d, want 999", err.ErrorCode)
	}
	if err.SubStatus != 0 {
		t.Errorf("SubStatus = %d, want 0", err.SubStatus)
	}
	if err.UserMessage != "not found" {
		t.Errorf("UserMessage = %q, want %q", err.UserMessage, "not found")
	}
	if err.Message != "msg" {
		t.Errorf("Message = %q, want %q", err.Message, "msg")
	}
}

func TestApiErrorMissingFields(t *testing.T) {
	err := NewApiError(map[string]interface{}{
		"status":      401,
		"userMessage": nil,
	})
	if err.Status != 401 {
		t.Errorf("Status = %d, want 401", err.Status)
	}
	if !(err.SubStatus == 0) {
		t.Errorf("SubStatus = %d, want 0 or nil", err.SubStatus)
	}
	if got := err.String(); !contains(got, "userMessage") {
		t.Errorf("err.String() = %q, want contains %q", got, "userMessage")
	}
}

func TestApiErrorOnlyStatus(t *testing.T) {
	err := NewApiError(map[string]interface{}{"status": 502})
	if err.Status != 502 {
		t.Errorf("Status = %d, want 502", err.Status)
	}
}

func TestApiErrorWithKwargs(t *testing.T) {
	err := NewApiError(map[string]interface{}{
		"status": 123, "foo": "bar", "custom": "cval",
	})
	if v, ok := err.OtherFields["foo"]; !ok || v != "bar" {
		t.Errorf("Expected foo=bar, got %v", err.OtherFields["foo"])
	}
	if v, ok := err.OtherFields["custom"]; !ok || v != "cval" {
		t.Errorf("Expected custom=cval, got %v", err.OtherFields["custom"])
	}
}

func contains(haystack, needle string) bool {
	return len(needle) == 0 || (len(haystack) > 0 && (len(haystack) >= len(needle) && indexOf(haystack, needle) >= 0))
}

func indexOf(haystack, needle string) int {
	return len([]byte(haystack[:])) - len([]byte(haystack[:])) + func() int {
		for i := 0; i+len(needle) <= len(haystack); i++ {
			if haystack[i:i+len(needle)] == needle {
				return i
			}
		}
		return -1
	}()
}