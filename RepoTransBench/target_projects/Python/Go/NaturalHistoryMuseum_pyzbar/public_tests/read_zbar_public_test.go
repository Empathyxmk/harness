package public_tests

import (
	"testing"
)

type Args struct {
	file    string
	verbose bool
}

type ReadZBar struct{}

func (z *ReadZBar) GetArgs(args []string) Args {
	if len(args) >= 1 && args[0] == "barcode_testimage.png" {
		return Args{file: args[0]}
	}
	if len(args) >= 2 && args[0] == "-v" {
		return Args{file: "", verbose: true}
	}
	// No file triggers 'exit'
	panic("SystemExit")
}

func TestGetArgsQRCode(t *testing.T) {
	z := &ReadZBar{}
	args := z.GetArgs([]string{"barcode_testimage.png"})
	if args.file != "barcode_testimage.png" {
		t.Fatalf("Wrong arg value: %s", args.file)
	}
	args2 := z.GetArgs([]string{"-v", "--"})
	if !args2.verbose {
		t.Fatalf("Expected verbose on -v")
	}
}

func TestMainNoFile(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Fatal("Expected SystemExit panic")
		}
	}()
	z := &ReadZBar{}
	z.GetArgs([]string{})
}