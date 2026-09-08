package public_tests

import (
	"testing"

	"not_harshhaa_into_the_devops/syntaxlint"
)

func TestParseTagsPublic(t *testing.T) {
	t.Run("empty file", func(t *testing.T) {
		result := syntaxlint.ParseTags([]string{}, "public_empty.md")
		if len(result) != 0 {
			t.Errorf("expected empty list for empty input, got %d", len(result))
		}
	})

	t.Run("single valid detail block", func(t *testing.T) {
		lines := []string{
			"<details>",
			"<summary>This is a new public summary</summary>",
			"Public content goes here.",
			"</details>",
		}
		result := syntaxlint.ParseTags(lines, "file_public.md")
		expected := []syntaxlint.Tag{
			{
				Summary:  "This is a new public summary",
				Content:  "Public content goes here.",
				Start:    0,
				End:      3,
				Filename: "file_public.md",
			},
		}
		if len(result) != len(expected) {
			t.Fatalf("expected one tag, got %d", len(result))
		}
		got := result[0]
		want := expected[0]
		if got.Summary != want.Summary || got.Content != want.Content || got.Start != want.Start || got.End != want.End || got.Filename != want.Filename {
			t.Errorf("got %+v, want %+v", got, want)
		}
	})

	t.Run("detail block missing end", func(t *testing.T) {
		lines := []string{
			"<details>",
			"<summary>Public missing close</summary>",
			"Some content",
		}
		result := syntaxlint.ParseTags(lines, "public_missingend.md")
		if len(result) != 0 {
			t.Errorf("expected empty result for missing </details>, got %v", result)
		}
	})

	t.Run("multiple blocks with invalid one", func(t *testing.T) {
		lines := []string{
			"<details>",
			"<summary>Block A</summary>",
			"Alpha content.",
			"</details>",
			"<details>",
			"Oops",
			"Content without summary",
			"</details>",
			"<details>",
			"<summary>Block B</summary>",
			"Beta content.",
			"</details>",
		}
		result := syntaxlint.ParseTags(lines, "multi_public.md")
		if len(result) != 2 {
			t.Fatalf("expected 2 tags, got %d", len(result))
		}
		if result[0].Summary != "Block A" || result[1].Summary != "Block B" {
			t.Errorf("expected Block A and Block B summaries, got %s and %s", result[0].Summary, result[1].Summary)
		}
	})

	t.Run("detail block with content", func(t *testing.T) {
		lines := []string{
			"<details>",
			"<summary>Alternate summary</summary>",
			"First public line.",
			"Second public line.",
			"</details>",
		}
		result := syntaxlint.ParseTags(lines, "cpublic.md")
		if result[0].Content != "First public line.\nSecond public line." {
			t.Errorf("expected concatenated lines for content, got %q", result[0].Content)
		}
	})
}

func TestFormattingChecksPublic(t *testing.T) {
	t.Run("valid detail format", func(t *testing.T) {
		tags := []syntaxlint.Tag{
			{
				Summary:  "A public summary",
				Content:  "A content detail.",
				Start:    20,
				End:      23,
				Filename: "another_public.md",
			},
		}
		errors := syntaxlint.CheckFormatting(tags)
		if len(errors) != 0 {
			t.Errorf("expected no errors for valid detail, got %v", errors)
		}
	})

	t.Run("missing summary", func(t *testing.T) {
		tags := []syntaxlint.Tag{
			{
				Summary:  "",
				Content:  "Content that's public and missing summary.",
				Start:    150,
				End:      159,
				Filename: "no_public_summary.md",
			},
		}
		errors := syntaxlint.CheckFormatting(tags)
		found := false
		for _, e := range errors {
			if containsIgnoreCase(e, "missing summary") {
				found = true
			}
		}
		if !found {
			t.Errorf("expected error about missing summary, got %v", errors)
		}
	})

	t.Run("mismatched tags", func(t *testing.T) {
		tags := []syntaxlint.Tag{
			{
				Summary:  "public fail",
				Content:  "content",
				Start:    9,
				End:      -1, // None in python, -1 in Go for missing
				Filename: "badtag_public_2.md",
			},
		}
		errors := syntaxlint.CheckFormatting(tags)
		found := false
		for _, e := range errors {
			if containsIgnoreCase(e, "mismatched") || containsIgnoreCase(e, "unterminated") {
				found = true
			}
		}
		if !found {
			t.Errorf("expected error about mismatched/unterminated tags, got %v", errors)
		}
	})
}

func containsIgnoreCase(s, substr string) bool {
	return len(s) >= len(substr) && (lower(s).Contains(lower(substr)))
}
func lower(s string) string {
	return string([]rune(s))
}