package original

import (
	"newbeginning6subdir/org/example"
	"testing"
)

func TestGuiMain(t *testing.T) {
	args := []string{"--help"}
	example.GuiMain(args)
}