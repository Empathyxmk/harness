package public_tests

import (
	"bufio"
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"testing"
)

type DummyPublicFastqRecord struct {
	Name string
}
func NewDummyPublicFastqRecord(n string) DummyPublicFastqRecord {
	return DummyPublicFastqRecord{Name: n}
}

type Pairomatic struct {}

func getFastqNames(filePath string, delimiter *rune) (map[string]struct{}, error) {
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
			}
			names[name] = struct{}{}
		}
		// Fastq skips next 3 lines
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
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func createTempFastq(names []string, delimiter *rune) (string, error) {
	tmpF, err := ioutil.TempFile("", "pairo_pub.fastq")
	if err != nil {
		return "", err
	}
	defer tmpF.Close()
	for _, n := range names {
		suffix := ""
		if delimiter != nil {
			suffix = string(*delimiter) + "2"
		}
		tmpF.WriteString(fmt.Sprintf("@%s%s\nTGCA\n+\n@@@@\n", n, suffix))
	}
	return tmpF.Name(), nil
}

func TestGetFastqNamesDelimiterDash(t *testing.T) {
	p := Pairomatic{}
	names := []string{"QX", "ZE"}
	delim := '-'
	f, err := createTempFastq(names, &delim)
	if err != nil {
		t.Fatalf("createTempFastq failed: %v", err)
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

func TestGetFastqNamesNoDelimiterMultiple(t *testing.T) {
	p := Pairomatic{}
	names := []string{"A010", "B020"}
	f, err := createTempFastq(names, nil)
	if err != nil {
		t.Fatalf("createTempFastq failed: %v", err)
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

func TestGetFastqNamesFailOnDelimiter(t *testing.T) {
	p := Pairomatic{}
	names := []string{"NM"}
	f, err := createTempFastq(names, nil)
	if err != nil {
		t.Fatalf("createTempFastq failed: %v", err)
	}
	defer os.Remove(f)
	delim := '-'
	_, err = getFastqNames(f, &delim)
	if err == nil || !strings.Contains(err.Error(), "Failed to find expected delimiter") {
		t.Errorf("Expected failure to find delimiter, got err: %v", err)
	}
}

func TestEqualOrderingMismatch(t *testing.T) {
	p := Pairomatic{}
	s1 := []string{"U", "V"}
	s2 := []string{"V", "U"}
	if equalOrdering(s1, s2) {
		t.Error("Should not be equal ordering for mismatched order")
	}
	s3 := []string{"U", "V"}
	if !equalOrdering(s1, s3) {
		t.Error("Should be equal ordering for identical sets")
	}
}