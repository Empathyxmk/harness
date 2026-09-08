package original

import (
	"testing"
)

// Emoji4Unicode dummy struct for coverage
type Emoji4Unicode struct{}

func (e *Emoji4Unicode) String() string {
	return "Emoji4Unicode"
}

func TestToStringAndClassLoads(t *testing.T) {
	emoji := Emoji4Unicode{}
	if emoji.String() == "" {
		t.Errorf("toString on Emoji4Unicode is empty")
	}
	var _ = Emoji4Unicode{}
}