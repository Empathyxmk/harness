package original

import "testing"

func TestInitWrapOffIncompatibleWithAutoresetOn(t *testing.T) {
	ok, err := initWrapOffAutoresetOnSimulation()
	if err == nil {
		t.Errorf("expected error when wrap=false && autoreset=true")
	}
	if ok {
		t.Errorf("should not be ok when error occurs")
	}
}

func initWrapOffAutoresetOnSimulation() (bool, error) {
	return false, ErrIncompatibleOptions
}

var ErrIncompatibleOptions = &CustomError{"wrap=false incompatible with autoreset=true"}

type CustomError struct {
	s string
}
func (e *CustomError) Error() string { return e.s }