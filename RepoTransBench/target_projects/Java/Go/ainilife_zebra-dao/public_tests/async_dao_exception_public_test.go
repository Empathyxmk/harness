package public_tests

import "testing"

type AsyncDaoExceptionPublicTest struct {
	Msg string
}

func (e *AsyncDaoExceptionPublicTest) Error() string {
	return e.Msg
}

func TestAsyncDaoExceptionPublic_Message(t *testing.T) {
	ex := AsyncDaoExceptionPublicTest{"testPublicMsg"}
	if ex.Error() != "testPublicMsg" {
		t.Errorf("expected 'testPublicMsg', got %v", ex.Error())
	}
}