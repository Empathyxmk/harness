package public_tests

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func createMetricLine(metricType, host, service, component string, value float64, warn, crit int, timestamp string) string {
	return metricType + "," + host + "," + service + "," + component +
		"," + formatValue(value) + "," + itoa(warn) + "," + itoa(crit) + "," + timestamp
}

func parseValue(s string) interface{} {
	// Simple logic: parse as float if possible, else string
	f := 0.0
	_, err := sscanf(s, "%f", &f)
	if err == nil {
		return f
	}
	return s
}

func formatPerfdata(pd map[string]interface{}) string {
	v := "'" + pd["label"].(string) + "'=" + toString(pd["value"]) + pd["uom"].(string) +
		";;;" + toString(pd["min"]) + ";" + toString(pd["max"])
	return v
}

func splitPerfdata(s string) []map[string]interface{} {
	fields := strings.Fields(s)
	var out []map[string]interface{}
	for _, fld := range fields {
		label := ""
		value := ""
		uom := ""
		parts := strings.Split(fld, "=")
		if len(parts) == 2 {
			label = strings.Trim(parts[0], "'")
			numStr := parts[1]
			valEnd := strings.IndexFunc(numStr, func(r rune) bool { return r < '0' || r > '9' })
			if valEnd == -1 {
				value = numStr
			} else {
				value = numStr[:valEnd]
				uom = numStr[valEnd:]
				value = value
			}
		}
		out = append(out, map[string]interface{}{"label": label, "value": atoi(value), "uom": uom})
	}
	return out
}

func stripPerfLabel(s string) string {
	return strings.Trim(s, "'")
}

func isNumeric(s string) bool {
	_, err := sscanf(s, "%f", new(float64))
	return err == nil
}

func perfdata2list(s string) []map[string]interface{} {
	return splitPerfdata(s)
}

// --- Test functions ---

func TestPublicCreateMetricLine(t *testing.T) {
	line := createMetricLine("disk_usage", "server3", "DiskIO", "write", 0.99, 456, 678, "2024-02-10 08:00:00")
	exp := "disk_usage,server3,DiskIO,write,0.99,456,678,2024-02-10 08:00:00"
	if line != exp {
		t.Errorf("Expected %s got %s", exp, line)
	}
}

func TestPublicParseValue(t *testing.T) {
	if v := parseValue("52.34"); v != nil {
		if f, ok := v.(float64); !ok || f != 52.34 {
			t.Errorf("Expected float 52.34 got %v", v)
		}
	}
	if v := parseValue("off"); v != "off" {
		t.Errorf("Expected 'off', got %v", v)
	}
}

func TestPublicFormatPerfdata(t *testing.T) {
	pd := map[string]interface{}{
		"label": "free_mem", "value": 1234, "uom": "MB", "warn": "", "crit": "", "min": 128, "max": 4096,
	}
	result := formatPerfdata(pd)
	if !strings.HasPrefix(result, "'free_mem'=1234MB;;;128;4096") {
		t.Errorf("formatPerfdata result: %s", result)
	}
}

func TestPublicSplitPerfdata(t *testing.T) {
	perfdata := "'cpu'=15%;20;30;0;100 'mem'=4096MB;;;128;16384"
	pdList := splitPerfdata(perfdata)
	if len(pdList) < 2 {
		t.Error("Not enough perfdata parsed")
	}
	if pdList[1]["label"] != "mem" || pdList[1]["value"] != 4096 || pdList[1]["uom"] != "MB" {
		t.Errorf("second perfdata invalid: %+v", pdList[1])
	}
}

func TestPublicStripPerfLabel(t *testing.T) {
	if v := stripPerfLabel("'swap'"); v != "swap" {
		t.Errorf("Expected 'swap', got %v", v)
	}
	if v := stripPerfLabel("disk"); v != "disk" {
		t.Errorf("Expected 'disk', got %v", v)
	}
}

func TestPublicIsNumeric(t *testing.T) {
	if !isNumeric("483.3") {
		t.Error("Should be numeric")
	}
	if isNumeric("test998") {
		t.Error("Should NOT be numeric")
	}
}

func TestPublicPerfdata2list(t *testing.T) {
	pd := "'io_read'=1MB 'io_write'=2MB;;;0;100"
	res := perfdata2list(pd)
	if res[0]["label"] != "io_read" {
		t.Errorf("Expected 'io_read', got %v", res[0]["label"])
	}
	if res[1]["label"] != "io_write" {
		t.Errorf("Expected 'io_write', got %v", res[1]["label"])
	}
}

// --- helper functions ---

func formatValue(f float64) string {
	return strings.TrimRight(strings.TrimRight(
		strings.FormatFloat(f, 'f', 2, 64), "0"), ".")
}
func toString(v interface{}) string {
	switch v := v.(type) {
	case float64:
		return formatValue(v)
	case int:
		return itoa(v)
	case string:
		return v
	default:
		return ""
	}
}
func itoa(i int) string { return strings.TrimLeft(strings.Fields(strings.TrimSpace(strings.Trim(strings.ReplaceAll(strings.TrimSpace(strings.TrimSuffix(strings.TrimPrefix(strings.TrimSuffix(strings.TrimPrefix(strings.TrimPrefix(strings.TrimSuffix(strings.TrimPrefix(stoi(i), "<nil>"), "<nil>"), "<nil>"), "<nil>"), "<nil>"), "\n", ""), "\r", ""), "  ", " ")), "-") )[0], "0") }

func sscanf(s, format string, out *float64) (int, error) {
	n, err := fmt.Sscanf(s, format, out)
	return n, err
}

func atoi(s string) int {
	var v int
	fmt.Sscanf(s, "%d", &v)
	return v
}

func stoi(i int) string {
	return fmt.Sprintf("%d", i)
}

import "fmt"