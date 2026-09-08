package original

import (
	"bufio"
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"testing"
)

// DummyFastqRecord for test use
type DummyFastqRecord struct {
	Name string
}
func NewDummyFastqRecord(n string) DummyFastqRecord {
	return DummyFastqRecord{Name: n}
}

// Mocks for Pairomatic functions
type Pairomatic struct{}

func getFastqNames(filePath string, delimiter *rune) (map[string]struct{}, error) {
	// Parse file and extract record names.
	f, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	names := make(map[string]struct{})
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := scanner.Text()
		if strings.HasPrefix(line, "@") {
			name := strings.TrimPrefix(line, "@")
			if delimiter != nil {
				parts := strings.SplitN(name, string(*delimiter), 2)
				if len(parts) != 2 {
					return nil, fmt.Errorf("Failed to find expected delimiter")
				}
				name = parts[0]
			} else {
				// delimiter nil, just name
			}
			names[name] = struct{}{}
		}
		// Skip next 3 lines
		for i := 0; i < 3; i++ {
			if !scanner.Scan() {
				return nil, errors.New("Malformed fastq file")
			}
		}
	}
	return names, nil
}
func equalOrdering(a, b []string) bool {
	if len(a) != len(b) {
		return false
	}
	for i, v := range a {
		if b[i] != v {
			return false
		}
	}
	return true
}

func createFastqFile(names []string, delimiter *rune) (string, error) {
	tmpF, err := ioutil.TempFile("", "pairo.fastq")
	if err != nil {
		return "", err
	}
	defer tmpF.Close()
	for _, n := range names {
		suffix := ""
		if delimiter != nil {
			suffix = string(*delimiter) + "1"
		}
		tmpF.WriteString(fmt.Sprintf("@%s%s\nACGT\n+\n!!!!\n", n, suffix))
	}
	return tmpF.Name(), nil
}

func TestGetFastqNamesNoDelimiter(t *testing.T) {
	p := Pairomatic{}
	names := []string{"x1", "y2"}
	f, err := createFastqFile(names, nil)
	if err != nil {
		t.Fatalf("failed createFastqFile: %v", err)
	}
	defer os.Remove(f)
	result, err := getFastqNames(f, nil)
	if err != nil {
		t.Fatalf("getFastqNames failed: %v", err)
	}
	if len(result) != 2 {
		t.Errorf("Expected 2 names, got %d", len(result))
	}
}

func TestGetFastqNamesWithDelimiter(t *testing.T) {
	p := Pairomatic{}
	names := []string{"A", "B"}
	delim := ':'
	f, err := createFastqFile(names, &delim)
	if err != nil {
		t.Fatalf("failed createFastqFile: %v", err)
	}
	defer os.Remove(f)
	result, err := getFastqNames(f, &delim)
	if err != nil {
		t.Fatalf("getFastqNames failed: %v", err)
	}
	if len(result) != 2 {
		t.Errorf("Expected 2 names, got %d", len(result))
	}
}

func TestGetFastqNamesDelimiterNotFound(t *testing.T) {
	p := Pairomatic{}
	names := []string{"Z"}
	f, err := createFastqFile(names, nil)
	if err != nil {
		t.Fatalf("failed createFastqFile: %v", err)
	}
	defer os.Remove(f)
	delim := ':'
	_, err = getFastqNames(f, &delim)
	if err == nil || !strings.Contains(err.Error(), "Failed to find expected delimiter") {
		t.Errorf("Expect error with delimiter missing, got: %v", err)
	}
}

func TestEqualOrdering(t *testing.T) {
	// The underlying sets are ordered lists for this test.
	s1 := []string{"A", "B"}
	s2 := []string{"A", "B"}
	if !equalOrdering(s1, s2) {
		t.Error("Expected equal ordering for identical input")
	}
	s3 := []string{"B", "A"}
	if equalOrdering(s1, s3) {
		t.Error("Should not be equal ordering if order differs")
	}
}