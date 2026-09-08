package original

import (
	"testing"
)

type Application struct{}

func TestApplicationTest(t *testing.T) {
	_ = &Application{}
	// Only verifies Application can be created.
}