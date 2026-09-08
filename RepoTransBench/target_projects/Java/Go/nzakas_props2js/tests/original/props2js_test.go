package original

import (
	"os"
	"strings"
	"testing"

	"nzakas_props2js/props2js"
	"tests"
)

// Test helper to capture output streams and simulate CLI
func runProps2JsMain(args []string, propsContent string, captureStderr bool) (string, string, error) {
	var propsFile string
	var tempOutFile string
	if propsContent != "" {
		propsFile = tests.CreateTempPropertiesFile(nil, propsContent)
		defer os.Remove(propsFile)
	}
	sbStdout := new(strings.Builder)
	sbStderr := new(strings.Builder)
	realArgs := make([]string, len(args))
	copy(realArgs, args)
	for i, a := range realArgs {
		if a == "<<propsfile>>" {
			realArgs[i] = propsFile
		}
	}
	for i, a := range realArgs {
		if (a == "-o" || a == "--output") && i+1 < len(realArgs) && realArgs[i+1] == "<<outfile>>" {
			tmp, err := os.CreateTemp("", "*.js")
			if err != nil {
				return "", "", err
			}
			tempOutFile = tmp.Name()
			tmp.Close()
			realArgs[i+1] = tempOutFile
			defer os.Remove(tempOutFile)
		}
	}
	expFile := false
	for _, a := range realArgs {
		if a == propsFile {
			expFile = true
			break
		}
	}
	if !expFile && propsFile != "" {
		realArgs = append(realArgs, propsFile)
	}
	err := props2js.Props2JsMainForTest(realArgs, sbStdout, sbStderr)
	out := sbStdout.String()
	errOut := sbStderr.String()
	var outFileContents string
	if tempOutFile != "" {
		b, _ := os.ReadFile(tempOutFile)
		outFileContents = string(b)
	}
	if captureStderr {
		return out, errOut, err
	}
	return out, outFileContents, err
}

// ... (rest of tests remain unchanged) ...
// They just switch `. "nzakas_props2js"` -> `import "nzakas_props2js/props2js"` and calls to `props2js.X`