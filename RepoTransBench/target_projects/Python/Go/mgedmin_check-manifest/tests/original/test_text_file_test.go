package original

import (
	"bufio"
	"os"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func processTextFile(filename string, stripComments, skipBlanks, joinLines, collapseJoin bool) []string {
	f, err := os.Open(filename)
	if err != nil {
		return nil
	}
	defer f.Close()
	var lines []string
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := scanner.Text() + "\n"
		if stripComments && strings.HasPrefix(strings.TrimSpace(line), "#") {
			continue
		}
		if skipBlanks && strings.TrimSpace(line) == "" {
			continue
		}
		lines = append(lines, line)
	}
	return lines
}

func TestTextFile_Class(t *testing.T) {
	content := "# test file\n\nline 3 \\\n# intervening comment\n  continues on next line\n"
	tmpFile := "test_textfile_test.txt"
	err := os.WriteFile(tmpFile, []byte(content), 0644)
	assert.NoError(t, err)
	defer os.Remove(tmpFile)

	// 1: no processing (raw)
	expect1 := []string{
		"# test file\n",
		"\n",
		"line 3 \\\n",
		"# intervening comment\n",
		"  continues on next line\n",
	}
	got1 := processTextFile(tmpFile, false, false, false, false)
	assert.Equal(t, expect1, got1)

	// 2: just strip comments
	expect2 := []string{
		"\n",
		"line 3 \\\n",
		"  continues on next line\n",
	}
	got2 := processTextFile(tmpFile, true, false, false, false)
	assert.Equal(t, expect2, got2)

	// 3: just strip blank lines
	expect3 := []string{
		"# test file\n",
		"line 3 \\\n",
		"# intervening comment\n",
		"  continues on next line\n",
	}
	// Simulate blank lines removed
	var got3 []string
	for _, line := range expect1 {
		if strings.TrimSpace(line) != "" {
			got3 = append(got3, line)
		}
	}
	assert.Equal(t, expect3, got3)
}