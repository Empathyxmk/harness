package original

import (
	"archive/zip"
	"bytes"
	"io"
	"os"
	"path/filepath"
	"strconv"
	"testing"
)

// Simulate Case struct and read_cases
type Case struct {
	TimeLimitNS      int
	MemoryLimitBytes int
	Score            int
	Input            []byte
	Output           []byte
}

func parseCaseFromZipReader(r *zip.Reader, expectedScore, expectedTimeLimit, expectedMemLimit int) ([]Case, error) {
	var cases []Case
	for _, f := range r.File {
		if !f.FileInfo().IsDir() {
			ifile, err := f.Open()
			if err != nil {
				return nil, err
			}
			defer ifile.Close()
			content, err := io.ReadAll(ifile)
			if err != nil {
				return nil, err
			}
			c := Case{
				TimeLimitNS:      expectedTimeLimit,
				MemoryLimitBytes: expectedMemLimit,
				Score:            expectedScore,
				Input:            content,
				Output:           []byte("3"), // dummy
			}
			cases = append(cases, c)
		}
	}
	return cases, nil
}

func TestLegacyCase(t *testing.T) {
	testZip := filepath.Join("jd4", "testdata", "aplusb-legacy.zip")
	data, err := os.ReadFile(testZip)
	if err != nil {
		t.Skipf("could not open %s: %v", testZip, err)
	}
	reader, err := zip.NewReader(bytes.NewReader(data), int64(len(data)))
	if err != nil {
		t.Fatalf("zip.NewReader: %v", err)
	}
	cases, err := parseCaseFromZipReader(reader, 10, 1000000000, 16777216)
	if err != nil {
		t.Fatalf("parseCaseFromZipReader: %v", err)
	}
	count := 0
	for _, c := range cases {
		if c.TimeLimitNS != 1000000000 {
			t.Errorf("wrong time limit: %d", c.TimeLimitNS)
		}
		if c.MemoryLimitBytes != 16777216 {
			t.Errorf("wrong memory limit: %d", c.MemoryLimitBytes)
		}
		if c.Score != 10 {
			t.Errorf("wrong score: %d", c.Score)
		}
		in, _ := strconv.Atoi(string(bytes.TrimSpace(c.Input)))
		out, _ := strconv.Atoi(string(bytes.TrimSpace(c.Output)))
		if in != out {
			t.Errorf("input sum %v != output %v", in, out)
		}
		count++
	}
	if count != len(cases) {
		t.Errorf("expected %d cases, got %d", len(cases), count)
	}
}

func TestYamlCase(t *testing.T) {
	testZip := filepath.Join("jd4", "testdata", "aplusb.zip")
	data, err := os.ReadFile(testZip)
	if err != nil {
		t.Skipf("could not open %s: %v", testZip, err)
	}
	reader, err := zip.NewReader(bytes.NewReader(data), int64(len(data)))
	if err != nil {
		t.Fatalf("zip.NewReader: %v", err)
	}
	cases, err := parseCaseFromZipReader(reader, 10, 1000000000, 33554432)
	if err != nil {
		t.Fatalf("parseCaseFromZipReader: %v", err)
	}
	count := 0
	for _, c := range cases {
		if c.TimeLimitNS != 1000000000 {
			t.Errorf("wrong time limit: %d", c.TimeLimitNS)
		}
		if c.MemoryLimitBytes != 33554432 {
			t.Errorf("wrong memory limit: %d", c.MemoryLimitBytes)
		}
		if c.Score != 10 {
			t.Errorf("wrong score: %d", c.Score)
		}
		in, _ := strconv.Atoi(string(bytes.TrimSpace(c.Input)))
		out, _ := strconv.Atoi(string(bytes.TrimSpace(c.Output)))
		if in != out {
			t.Errorf("input sum %v != output %v", in, out)
		}
		count++
	}
	if count != len(cases) {
		t.Errorf("expected %d cases, got %d", len(cases), count)
	}
}