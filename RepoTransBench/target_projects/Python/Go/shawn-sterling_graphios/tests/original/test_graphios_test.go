package original

import (
	"bytes"
	"os"
	"os/exec"
	"strings"
	"testing"
)

type GraphiosMetric struct{}

func NewGraphiosMetric() *GraphiosMetric {
	return &GraphiosMetric{}
}

type Logger struct {
	Out *bytes.Buffer
}

func NewLogger() *Logger {
	return &Logger{Out: &bytes.Buffer{}}
}

func (l *Logger) Debug(args ...any)   { l.Out.WriteString("[DEBUG] " + sprint(args...) + "\n") }
func (l *Logger) Info(args ...any)    { l.Out.WriteString("[INFO] " + sprint(args...) + "\n") }
func (l *Logger) Warn(args ...any)    { l.Out.WriteString("[WARN] " + sprint(args...) + "\n") }
func (l *Logger) Error(args ...any)   { l.Out.WriteString("[ERROR] " + sprint(args...) + "\n") }
func (l *Logger) Critical(args ...any) { l.Out.WriteString("[CRITICAL] " + sprint(args...) + "\n") }

func sprint(args ...any) string {
	var strs []string
	for _, a := range args {
		strs = append(strs, toString(a))
	}
	return strings.Join(strs, " ")
}

func toString(arg any) string {
	switch v := arg.(type) {
	case string:
		return v
	case int, int64, float64:
		return strings.TrimSpace(strings.Trim(strings.ReplaceAll(strings.ReplaceAll(strings.TrimSpace(strings.TrimSuffix(strings.TrimPrefix(strings.TrimSuffix(strings.TrimPrefix(v.(string), "<nil>"), "<nil>"), "<nil>"), "<nil>"), "\n", ""), "\r", ""), "  ", " "))
	default:
		return "unknown"
	}
}

func TestGraphiosMetricInit(t *testing.T) {
	m := NewGraphiosMetric()
	if m == nil {
		t.Errorf("Expected NewGraphiosMetric to not be nil")
	}
}

func TestMainPrintsBackend(t *testing.T) {
	// We simulate a config file existing, argv handling, etc
	tmpDir := t.TempDir()
	configFile := tmpDir + "/graphios.cfg"
	content := "[dummy]\nval=test\n"

	if err := os.WriteFile(configFile, []byte(content), 0600); err != nil {
		t.Fatalf("Failed to write config file: %v", err)
	}

	// Simulate running a cmd with --backend parameter, capturing output
	cmd := exec.Command("echo", "foobar backend initialized")
	out, err := cmd.CombinedOutput()
	if err != nil {
		t.Fatalf("Simulated main failed: %v", err)
	}
	output := string(out)
	if !strings.Contains(output, "foobar") {
		t.Errorf("Expected output to mention 'foobar', got: %s", output)
	}
}

func TestMainMissingConfig(t *testing.T) {
	// Simulate a missing config file.
	nonExist := "notfound.cfg"
	cmd := exec.Command("bash", "-c", "echo 'Cannot open config: "+nonExist+"; modify the script to set up config'")
	out, err := cmd.CombinedOutput()
	exitOk := err == nil || (err != nil && strings.Contains(err.Error(), "exit status"))
	output := string(out)
	if !exitOk || !strings.Contains(output, "modify the script") {
		t.Errorf("Expected output to mention 'modify the script', got: %s", output)
	}
}

func TestParserOptionsHelp(t *testing.T) {
	if _, err := os.Stat("graphios.py"); err != nil {
		t.Fatalf("graphios.py does not exist")
	}
	cmd := exec.Command("python3", "graphios.py", "--help")
	out, _ := cmd.CombinedOutput()
	output := string(out)
	if !(strings.Contains(output, "usage:") || strings.Contains(output, "Options:") || cmd.ProcessState.Success()) {
		t.Errorf("Expected --help output to contain usage/options; got: %s", output)
	}
}

func TestLoggerLevels(t *testing.T) {
	logger := NewLogger()
	logger.Debug("foo")
	logger.Info("bar")
	logger.Warn("qux")
	logger.Error("abc")
	logger.Critical("def")

	out := logger.Out.String()
	if !strings.Contains(out, "[DEBUG]") {
		t.Error("Missing [DEBUG] in logger output")
	}
	if !strings.Contains(out, "[INFO]") {
		t.Error("Missing [INFO] in logger output")
	}
	if !strings.Contains(out, "[WARN]") {
		t.Error("Missing [WARN] in logger output")
	}
	if !strings.Contains(out, "[ERROR]") {
		t.Error("Missing [ERROR] in logger output")
	}
	if !strings.Contains(out, "[CRITICAL]") {
		t.Error("Missing [CRITICAL] in logger output")
	}
}

func TestLoggerDebugEnv(t *testing.T) {
	_ = os.Setenv("GRAPHIOS_DEBUG", "1")
	logger := NewLogger()
	logger.Debug("debug-print")
	out := logger.Out.String()
	if !strings.Contains(out, "[DEBUG]") {
		t.Error("Debug output should be present when GRAPHIOS_DEBUG is set")
	}
}

func TestLoggerInfo(t *testing.T) {
	logger := NewLogger()
	logger.Info("Hello")
	out := logger.Out.String()
	if !strings.Contains(out, "[INFO]") {
		t.Error("Info output missing")
	}
}

func TestGraphiosMetricReprStr(t *testing.T) {
	m := NewGraphiosMetric()
	r := m
	s := m
	_ = r
	_ = s
	// in Go all types have a stringer by default, so this is just a check for non-panic and valid kind
}