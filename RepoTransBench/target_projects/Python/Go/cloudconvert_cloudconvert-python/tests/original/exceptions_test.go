package original

import (
	"fmt"
	"testing"
)

type CloudConvertException struct {
	Message string
}

func (e CloudConvertException) Error() string { return e.Message }

type ApiError struct {
	Message string
	code    int
}

func (e ApiError) Error() string { return e.Message }
func (e ApiError) Code() int     { return e.code }

type TimeoutException struct{ CloudConvertException }
type AuthException struct{ CloudConvertException }
type ParseException struct{ CloudConvertException }
type InvalidRequest struct{ CloudConvertException }
type InvalidResponse struct{ CloudConvertException }
type ConnectionFailed struct{ CloudConvertException }

func TestApiErrorStr(t *testing.T) {
	e := ApiError{"msg", 400}
	if !containsString(e.Error(), "msg") {
		t.Errorf("Expected 'msg' in error")
	}
	if e.Code() != 400 {
		t.Errorf("ApiError code 400 expected, got %v", e.Code())
	}
}

func TestTimeoutException(t *testing.T) {
	e := TimeoutException{CloudConvertException{"Timeouted!"}}
	if e.Error() != "Timeouted!" {
		t.Errorf("TimeoutException should be 'Timeouted!', got %v", e.Error())
	}
}

func TestAuthException(t *testing.T) {
	e := AuthException{CloudConvertException{"Unauthorized"}}
	if e.Error() != "Unauthorized" {
		t.Errorf("AuthException should be 'Unauthorized', got %v", e.Error())
	}
}

func TestParseException(t *testing.T) {
	e := ParseException{CloudConvertException{"bad parse"}}
	if e.Error() != "bad parse" {
		t.Errorf("ParseException should be 'bad parse', got %v", e.Error())
	}
}

func TestInvalidRequest(t *testing.T) {
	e := InvalidRequest{CloudConvertException{"invalid"}}
	if e.Error() != "invalid" {
		t.Errorf("InvalidRequest should be 'invalid', got %v", e.Error())
	}
}

func TestInvalidResponse(t *testing.T) {
	e := InvalidResponse{CloudConvertException{"invalidresp"}}
	if e.Error() != "invalidresp" {
		t.Errorf("InvalidResponse should be 'invalidresp', got %v", e.Error())
	}
}

func TestConnectionFailed(t *testing.T) {
	e := ConnectionFailed{CloudConvertException{"fail"}}
	if e.Error() != "fail" {
		t.Errorf("ConnectionFailed should be 'fail', got %v", e.Error())
	}
}

// Helper
func containsString(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(s) > 0 && (containsString(s[1:], substr) || s[:len(substr)] == substr))
}