package original

import (
	"bufio"
	"bytes"
	"io"
	"os"
	"strings"
	"testing"
)

// Simulate the Convert class for testing (convert.go).
// Let's define two functions for demonstration:
func celsiusToFahrenheit(c float64) float64 {
	return c*9.0/5.0 + 32.0
}
func fahrenheitToCelsius(f float64) float64 {
	return (f - 32.0) * 5.0 / 9.0
}

// Simulate Convert.main's behavior (from src/test/java/ch03/ConvertTest.java)
func convertMain(input io.Reader, output io.Writer) {
	scanner := bufio.NewScanner(input)
	output.Write([]byte("Enter miles:"))
	if scanner.Scan() {
		line := scanner.Text()
		miles := 0.0
		_, err := fmt.Sscanf(line, "%f", &miles)
		if err != nil {
			output.Write([]byte("\nInvalid input for miles"))
			return
		}
		km := miles * 1.60934
		output.Write([]byte(fmt.Sprintf("\n%v miles is %v kilometers", miles, km)))
	}
}

func TestConvertMainWithNumericInput(t *testing.T) {
	input := strings.NewReader("10\n")
	var output bytes.Buffer
	convertMain(input, &output)
	outStr := strings.ToLower(output.String())
	if !strings.Contains(outStr, "miles") {
		t.Errorf("Prompt or output should mention miles, got %q", outStr)
	}
	if !strings.Contains(outStr, "kilometers") {
		t.Errorf("Output should mention kilometers, got %q", outStr)
	}
}

func TestConvertMainWithInvalidInput(t *testing.T) {
	input := strings.NewReader("foo\n")
	var output bytes.Buffer
	convertMain(input, &output)
	outStr := strings.ToLower(output.String())
	if !strings.Contains(outStr, "miles") {
		t.Errorf("Should prompt for miles even on bad input, got %q", outStr)
	}
}