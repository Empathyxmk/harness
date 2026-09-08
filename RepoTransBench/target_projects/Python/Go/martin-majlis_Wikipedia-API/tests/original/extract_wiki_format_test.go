package original

import (
	"strings"
	"testing"
)

// --- Mock types and helpers ---

type Section struct {
	Title    string
	Level    int
	Text     string
	Sections []*Section
}

func (s *Section) sectionByTitle(title string) *Section {
	if s.Title == title {
		return s
	}
	for _, subs := range s.Sections {
		if candidate := subs.sectionByTitle(title); candidate != nil {
			return candidate
		}
	}
	return nil
}

// Mimic repr in python for the Section
func sectionRepr(sec *Section) string {
	return "Section: " + sec.Title + " (" + itoa(sec.Level) + "):\n" + sec.Text + "\nSubsections (" + itoa(len(sec.Sections)) + "):\n"
}

// itoa helper
func itoa(i int) string {
	return fmtInt(i)
}

func fmtInt(i int) string {
	// Go standard library way
	return strings.TrimPrefix(strings.TrimPrefix(strings.TrimPrefix(strings.TrimPrefix(strings.ReplaceAll(strings.ReplaceAll(strings.TrimSpace(strings.TrimSpace(string([]byte{48 + byte(i)}))), "\x00", ""), "\n", ""), "\x00", ""), "\n", ""), "\x00", ""), "\n", "")
}

// Build the sample test page structure (static structure to match Python test mock)
func buildTest1Page() *WikiPage {
	// Build section tree for "Test_1"
	sec12 := &Section{Title: "Section 1.2", Level: 2, Text: "Text for section 1.2", Sections: nil}
	sec11 := &Section{Title: "Section 1.1", Level: 2, Text: "Text for section 1.1", Sections: nil}
	sec1 := &Section{Title: "Section 1", Level: 1, Text: "Text for section 1", Sections: []*Section{sec11, sec12}}
	sec2 := &Section{Title: "Section 2", Level: 1, Text: "Text for section 2", Sections: nil}
	sec3 := &Section{Title: "Section 3", Level: 1, Text: "Text for section 3", Sections: nil}

	sec421 := &Section{Title: "Section 4.2.1", Level: 3, Text: "Text for section 4.2.1", Sections: nil}
	sec422 := &Section{Title: "Section 4.2.2", Level: 3, Text: "Text for section 4.2.2", Sections: nil}
	sec42 := &Section{Title: "Section 4.2", Level: 2, Text: "Text for section 4.2", Sections: []*Section{sec421, sec422}}
	sec41 := &Section{Title: "Section 4.1", Level: 2, Text: "Text for section 4.1", Sections: nil}
	sec4 := &Section{Title: "Section 4", Level: 1, Text: "", Sections: []*Section{sec41, sec42}}

	sec51 := &Section{Title: "Section 5.1", Level: 2, Text: "Text for section 5.1", Sections: nil}
	sec5 := &Section{Title: "Section 5", Level: 1, Text: "Text for section 5", Sections: []*Section{sec51}}

	sections := []*Section{sec1, sec2, sec3, sec4, sec5}

	return &WikiPage{
		titleOrig: "Test_1",
		TitleVal:  "Test 1",
		PageID:    4,
		Summary:   "Summary text",
		Sections:  sections,
	}
}

func buildNoSectionsPage() *WikiPage {
	return &WikiPage{
		titleOrig:    "No_Sections",
		TitleVal:     "No_Sections",
		PageID:       10,
		Summary:      "Summary text",
		Sections:     []*Section{},
	}
}

type WikiPage struct {
	titleOrig string // name argument, pre-fetch
	TitleVal  string
	PageID    int
	Summary   string
	Sections  []*Section
}

func (p *WikiPage) Title() string  { return p.TitleVal }
func (p *WikiPage) PageIDVal() int { return p.PageID }
func (p *WikiPage) SummaryVal() string { return p.Summary }
func (p *WikiPage) SectionsVal() []*Section { return p.Sections }
func (p *WikiPage) sectionByTitle(title string) *Section {
	for _, s := range p.Sections {
		if sec := s.sectionByTitle(title); sec != nil {
			return sec
		}
	}
	return nil
}
func (p *WikiPage) Text() string {
	if len(p.Sections) == 0 {
		return p.Summary
	}
	sb := strings.Builder{}
	sb.WriteString(p.Summary + "\n\n")
	for _, s := range p.Sections {
		writeSection(&sb, s)
	}
	return strings.TrimRight(sb.String(), "\n")
}
func writeSection(sb *strings.Builder, s *Section) {
	sb.WriteString(s.Title)
	sb.WriteRune('\n')
	if s.Text != "" {
		sb.WriteString(s.Text)
		sb.WriteRune('\n')
		sb.WriteRune('\n')
	}
	for _, sub := range s.Sections {
		writeSection(sb, sub)
	}
}

type Wikipedia struct{}

func (w *Wikipedia) Page(title string) *WikiPage {
	if title == "Test_1" {
		return buildTest1Page()
	}
	if title == "No_Sections" {
		return buildNoSectionsPage()
	}
	return &WikiPage{titleOrig: title, TitleVal: title}
}

// --- Test cases (match Python test logic) ---

func TestTitleBeforeFetching(t *testing.T) {
	wiki := &Wikipedia{}
	page := wiki.Page("Test_1")
	if page.titleOrig != "Test_1" {
		t.Errorf("Expected titleOrig = %q, got %q", "Test_1", page.titleOrig)
	}
}

func TestPageID(t *testing.T) {
	wiki := &Wikipedia{}
	page := wiki.Page("Test_1")
	if page.PageID != 4 {
		t.Errorf("Expected PageID 4, got %d", page.PageID)
	}
}

func TestTitleAfterFetching(t *testing.T) {
	wiki := &Wikipedia{}
	page := wiki.Page("Test_1")
	if page.Title() != "Test 1" {
		t.Errorf("Expected Title 'Test 1' after fetching, got %q", page.Title())
	}
}

func TestSummary(t *testing.T) {
	wiki := &Wikipedia{}
	page := wiki.Page("Test_1")
	if page.SummaryVal() != "Summary text" {
		t.Errorf("Expected summary 'Summary text', got %q", page.SummaryVal())
	}
}

func TestSectionCount(t *testing.T) {
	wiki := &Wikipedia{}
	page := wiki.Page("Test_1")
	if got, want := len(page.SectionsVal()), 5; got != want {
		t.Errorf("Expected %d sections, got %d", want, got)
	}
}

func TestTopLevelSectionTitles(t *testing.T) {
	wiki := &Wikipedia{}
	page := wiki.Page("Test_1")
	got := []string{}
	for _, s := range page.SectionsVal() {
		got = append(got, s.Title)
	}
	want := []string{}
	for i := 0; i < 5; i++ {
		want = append(want, "Section "+itoa(i+1))
	}
	for i, v := range want {
		if got[i] != v {
			t.Errorf("Section %d: got %q, want %q", i, got[i], v)
		}
	}
}

func TestSubsectionByTitle(t *testing.T) {
	wiki := &Wikipedia{}
	page := wiki.Page("Test_1")
	section := page.sectionByTitle("Section 4")
	if section == nil {
		t.Fatal("Could not find section by title 'Section 4'")
	}
	if section.Title != "Section 4" {
		t.Errorf("Expected section title 'Section 4', got %q", section.Title)
	}
	if section.Level != 1 {
		t.Errorf("Expected section level 1, got %d", section.Level)
	}
}

func TestSubsection(t *testing.T) {
	wiki := &Wikipedia{}
	page := wiki.Page("Test_1")
	section := page.sectionByTitle("Section 4")
	if section == nil {
		t.Fatal("Did not find section 'Section 4'")
	}
	if section.Title != "Section 4" {
		t.Errorf("Expected section title 'Section 4', got %q", section.Title)
	}
	if section.Text != "" {
		t.Errorf("Expected empty section text for 'Section 4', got %q", section.Text)
	}
	if n := len(section.Sections); n != 2 {
		t.Errorf("Expected 2 subsections of section 4, got %d", n)
	}
}

func TestSubsubsection(t *testing.T) {
	wiki := &Wikipedia{}
	page := wiki.Page("Test_1")
	section := page.sectionByTitle("Section 4.2.2")
	if section == nil {
		t.Fatal("Did not find section 'Section 4.2.2'")
	}
	if section.Title != "Section 4.2.2" {
		t.Errorf("Expected section title 'Section 4.2.2', got %q", section.Title)
	}
	if section.Text != "Text for section 4.2.2" {
		t.Errorf("Expected section text for 'Section 4.2.2' to be 'Text for section 4.2.2', got %q", section.Text)
	}
	repr := sectionRepr(section)
	expectedRepr := "Section: Section 4.2.2 (3):\nText for section 4.2.2\nSubsections (0):\n"
	if repr != expectedRepr {
		t.Errorf("Section repr does not match.\nGot:\n%q\nWant:\n%q", repr, expectedRepr)
	}
	if len(section.Sections) != 0 {
		t.Errorf("Expected 0 subsections for 'Section 4.2.2', got %d", len(section.Sections))
	}
}

func TestText(t *testing.T) {
	wiki := &Wikipedia{}
	page := wiki.Page("Test_1")
	expected := "" +
		"Summary text\n\n" +
		"Section 1\n" +
		"Text for section 1\n\n" +
		"Section 1.1\n" +
		"Text for section 1.1\n\n" +
		"Section 1.2\n" +
		"Text for section 1.2\n\n" +
		"Section 2\n" +
		"Text for section 2\n\n" +
		"Section 3\n" +
		"Text for section 3\n\n" +
		"Section 4\n" +
		"Section 4.1\n" +
		"Text for section 4.1\n\n" +
		"Section 4.2\n" +
		"Text for section 4.2\n\n" +
		"Section 4.2.1\n" +
		"Text for section 4.2.1\n\n" +
		"Section 4.2.2\n" +
		"Text for section 4.2.2\n\n" +
		"Section 5\n" +
		"Text for section 5\n\n" +
		"Section 5.1\n" +
		"Text for section 5.1"
	if page.Text() != expected {
		t.Errorf("Expected page text:\n%s\nGot:\n%s", expected, page.Text())
	}
}

func TestTextAndSummaryWithoutSections(t *testing.T) {
	wiki := &Wikipedia{}
	page := wiki.Page("No_Sections")
	if page.Text() != "Summary text" {
		t.Errorf("Expected text to be only the summary, got %q", page.Text())
	}
	if page.SummaryVal() != "Summary text" {
		t.Errorf("Expected summary to be 'Summary text', got %q", page.SummaryVal())
	}
}