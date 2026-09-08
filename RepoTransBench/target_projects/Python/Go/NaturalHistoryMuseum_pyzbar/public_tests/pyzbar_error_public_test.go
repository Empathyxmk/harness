package public_tests

import "testing"

type PyzbarError struct {
	message string
}

func (e *PyzbarError) Error() string {
	return e.message
}

func TestErrorMessage(t *testing.T) {
	e := &PyzbarError{"Public test: barcode problem"}
	if e.Error() != "Public test: barcode problem" {
		t.Errorf("unexpected error message")
	}
}

func TestErrorRaiseAndCatch(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic")
		} else {
			if err, ok := r.(*PyzbarError); ok {
				if !contains(err.Error(), "catching") {
					t.Errorf("expected 'catching' in error message")
				}
			}
		}
	}()
	panic(&PyzbarError{"Test error for catching"})
}
func contains(s, sub string) bool {
	return len(sub) == 0 || len(s) >= len(sub) && (s == sub || contains(s[1:], sub))
}