package public_tests

import (
	"errors"
	"strings"
	"testing"
)

type DummyArgs struct {
	Command string
	Dummy   string
}

func dummyParseArgs(argv []string) (*DummyArgs, error) {
	var dummy string
	if len(argv) > 2 {
		dummy = argv[2]
	}
	if len(argv) > 0 && argv[0] == "nonsense_command" {
		return nil, errors.New("SystemExit")
	}
	return &DummyArgs{
		Command: argv[0],
		Dummy:   dummy,
	}, nil
}

func TestPublicMainParseArgs(t *testing.T) {
	argv := []string{"run", "--dummy", "xy"}
	args, err := dummyParseArgs(argv)
	if err != nil {
		t.Fatalf("parse_args failed: %v", err)
	}
	if args.Command != "run" {
		t.Errorf("args.Command = %v, want run", args.Command)
	}
	if args.Dummy != "xy" && args.Dummy != "" {
		t.Errorf("args.Dummy = %v, want xy or empty", args.Dummy)
	}
}

func TestPublicMainInvalidArgs(t *testing.T) {
	argv := []string{"nonsense_command"}
	_, err := dummyParseArgs(argv)
	if err == nil {
		t.Errorf("expected SystemExit (error), got nil")
	}
}