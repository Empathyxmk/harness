package original

import (
	"errors"
	"os"
	"strings"
	"testing"
)

type FileBackend struct {
	file string
	data *string
}

func (fb *FileBackend) SendMetric(m *FakeMetric) error {
	// Simulate writing a metric to a file
	record := m.host + " " + m.service + " " + m.metric + " " + m.value + " " + m.timestamp + "\n"
	if fb.data != nil {
		*fb.data += record
	}
	if fb.file != "" {
		return os.WriteFile(fb.file, []byte(record), 0600)
	}
	return nil
}

type CarbonBackend struct {
	host string
	port int
	data *string
}

func (cb *CarbonBackend) SendMetric(m *FakeMetric) error {
	if cb.data != nil {
		*cb.data += m.host + "." + m.service + "." + m.metric + " " + m.value + " " + m.timestamp + "\n"
	}
	return nil
}

type UDPSendBackend struct {
	host string
	port int
	data *string
}

func (ub *UDPSendBackend) SendMetric(m *FakeMetric) error {
	if ub.data != nil {
		*ub.data += m.host + "." + m.service + "." + m.metric + " " + m.value + " " + m.timestamp + "\n"
	}
	return nil
}

func loadBackend(kind string, args ...any) (any, error) {
	switch kind {
	case "file":
		var path string
		if len(args) > 0 {
			path, _ = args[0].(string)
		}
		return &FileBackend{file: path}, nil
	case "carbon":
		host, _ := args[0].(string)
		port, _ := args[1].(int)
		return &CarbonBackend{host: host, port: port}, nil
	case "udp":
		host, _ := args[0].(string)
		port, _ := args[1].(int)
		return &UDPSendBackend{host: host, port: port}, nil
	default:
		return nil, errors.New("invalid backend")
	}
}

type FakeMetric struct {
	host     string
	service  string
	metric   string
	value    string
	timestamp string
}

func TestLoadBackendInvalid(t *testing.T) {
	_, err := loadBackend("doesnotexist")
	if err == nil {
		t.Errorf("Expected error loading invalid backend")
	}
}

func TestLoadBackendFile(t *testing.T) {
	back, err := loadBackend("file", "/tmp/testfile")
	if err != nil {
		t.Fatalf("loadBackend failed: %v", err)
	}
	if _, ok := back.(*FileBackend); !ok {
		t.Errorf("Expected type FileBackend, got %T", back)
	}
}

func TestLoadBackendCarbon(t *testing.T) {
	back, err := loadBackend("carbon", "host", 1234)
	if err != nil {
		t.Fatalf("loadBackend failed: %v", err)
	}
	if _, ok := back.(*CarbonBackend); !ok {
		t.Errorf("Expected type CarbonBackend, got %T", back)
	}
}

func TestLoadBackendUDP(t *testing.T) {
	back, err := loadBackend("udp", "host", 1001)
	if err != nil {
		t.Fatalf("loadBackend failed: %v", err)
	}
	if _, ok := back.(*UDPSendBackend); !ok {
		t.Errorf("Expected type UDPSendBackend, got %T", back)
	}
}

func TestFileBackendSendMetric(t *testing.T) {
	tmp := t.TempDir()
	outfile := tmp + "/outfile"
	metric := &FakeMetric{
		host: "a", service: "b", metric: "c", value: "1", timestamp: "2",
	}
	back := &FileBackend{file: outfile}
	if err := back.SendMetric(metric); err != nil {
		t.Fatalf("FileBackend.SendMetric failed: %v", err)
	}
	data, err := os.ReadFile(outfile)
	if err != nil {
		t.Fatalf("Error reading outfile: %v", err)
	}
	if !strings.Contains(string(data), "a b c 1 2") {
		t.Errorf("Expected metric line in output: got %q", string(data))
	}
}

func TestCarbonBackendSendMetric(t *testing.T) {
	metric := &FakeMetric{host: "h", service: "s", metric: "m", value: "5", timestamp: "18"}
	results := ""
	back := &CarbonBackend{host: "test.host", port: 2003, data: &results}
	err := back.SendMetric(metric)
	if err != nil {
		t.Fatalf("CarbonBackend.SendMetric failed: %v", err)
	}
	if !strings.Contains(results, "h.s.m 5 18") {
		t.Errorf("Expected carbon metric string in %q", results)
	}
}

func TestUDPBackendSendMetric(t *testing.T) {
	metric := &FakeMetric{host: "hosty", service: "svc", metric: "metric", value: "3", timestamp: "6"}
	results := ""
	back := &UDPSendBackend{host: "testhost", port: 2222, data: &results}
	err := back.SendMetric(metric)
	if err != nil {
		t.Fatalf("UDPSendBackend.SendMetric failed: %v", err)
	}
	if !strings.Contains(results, "hosty.svc.metric 3 6") {
		t.Errorf("Expected udp metric string in %q", results)
	}
}