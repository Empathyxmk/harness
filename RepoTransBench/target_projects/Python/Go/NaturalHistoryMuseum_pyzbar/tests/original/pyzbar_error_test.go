package original

import "testing"

type PyZbarError struct {
	message string
}

func (e *PyZbarError) Error() string {
	return e.message
}

func TestPyzbarErrorIsException(t *testing.T) {
	var _ error = &PyZbarError{}
}

func TestPyzbarErrorRaiseAndStr(t *testing.T) {
	e := &PyZbarError{message: "fail"}
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic")
		}
	}()
	panic(e)
}