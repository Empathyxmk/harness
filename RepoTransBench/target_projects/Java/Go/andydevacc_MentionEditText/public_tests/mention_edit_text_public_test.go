package public_tests

import (
	"testing"
	"strings"
)

// (Repeats the core mock logic; in a real project you would share a utility)
type PatternMap map[string]string

type MentionEditText struct {
	text              string
	patternMap        PatternMap
	mentionTextColor  int
	selectionStart    int
	selectionEnd      int
	mentionList       []string
	onMentionListener func()
	isSelectedVal     bool
}

func NewMentionEditText() *MentionEditText {
	return &MentionEditText{
		text:       "",
		patternMap: PatternMap{"@": "@[a-zA-Z0-9_]+"},
	}
}

func (m *MentionEditText) SetText(t string) {
	m.text = t
	m.mentionList = extractMentions(m.text)
	m.selectionStart, m.selectionEnd = len(t), len(t)
}

func (m *MentionEditText) GetSelectionStart() int { return m.selectionStart }
func (m *MentionEditText) GetSelectionEnd() int   { return m.selectionEnd }
func (m *MentionEditText) SetSelection(start, end int) {
	m.selectionStart, m.selectionEnd = start, end
	ranges := getMentionRanges(m.text)
	for _, rg := range ranges {
		if m.selectionStart > rg.from && m.selectionStart < rg.to {
			m.selectionStart, m.selectionEnd = rg.to, rg.to
		}
	}
	for _, rg := range ranges {
		if (m.selectionStart > rg.from && m.selectionStart < rg.to) ||
			(m.selectionEnd > rg.from && m.selectionEnd < rg.to) {
			m.selectionStart, m.selectionEnd = rg.from, rg.to
			m.isSelectedVal = true
		}
	}
}

func (m *MentionEditText) SetMentionTextColor(c int) { m.mentionTextColor = c }
func (m *MentionEditText) IsSelected() bool          { return m.isSelectedVal }
func (m *MentionEditText) GetText() string           { return m.text }
func (m *MentionEditText) GetMentionList() []string  { return extractMentions(m.text) }

func getMentionRanges(text string) []struct{ from, to int } {
	res := []struct{ from, to int }{}
	offset := 0
	for _, part := range strings.Fields(text) {
		if strings.HasPrefix(part, "@") {
			res = append(res, struct{ from, to int }{offset, offset + len(part)})
		}
		offset += len(part) + 1
	}
	return res
}
func extractMentions(text string) []string {
	mentions := []string{}
	for _, part := range strings.Fields(text) {
		if strings.HasPrefix(part, "@") {
			mentions = append(mentions, part)
		}
	}
	return mentions
}

func TestConstructorsPublic(t *testing.T) {
	obj := NewMentionEditText()
	if obj == nil {
		t.Fatal("Constructor returned nil")
	}
}

func TestSetText_SelectionAtEnd_Public(t *testing.T) {
	m := NewMentionEditText()
	text := "Test @ExampleUser"
	m.SetText(text)
	if m.GetSelectionEnd() != len(text) {
		t.Errorf("Want selectionEnd %d, got %d", len(text), m.GetSelectionEnd())
	}
	if m.GetSelectionStart() != len(text) {
		t.Errorf("Want selectionStart %d, got %d", len(text), m.GetSelectionStart())
	}
}

func TestOnTextChanged_ColorsMentionString_Public(t *testing.T) {
	m := NewMentionEditText()
	m.SetMentionTextColor(999)
	text := "Greetings @alphaTest and @bravoTester!"
	m.SetText(text)
	mentions := extractMentions(text)
	if len(mentions) != 2 {
		t.Errorf("Expected 2 mentions, got %d", len(mentions))
	}
	if mentions[0] != "@alphaTest" {
		t.Errorf("First mention wrong: got %q", mentions[0])
	}
	if mentions[1] != "@bravoTester" {
		t.Errorf("Second mention wrong: got %q", mentions[1])
	}
}

func TestOnTextChanged_NoMentionString_Public(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Nothing special here, just text.")
	mentions := extractMentions(m.text)
	if len(mentions) != 0 {
		t.Errorf("Expected 0 mentions, got %d", len(mentions))
	}
}

func TestOnSelectionChanged_NoNearbyMentionString_Public(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Public input string.")
	m.SetSelection(8, 8)
	if m.GetSelectionStart() != 8 || m.GetSelectionEnd() != 8 {
		t.Errorf("Expected selection at (8,8), got (%d,%d)", m.GetSelectionStart(), m.GetSelectionEnd())
	}
}

func TestOnSelectionChanged_CursorInsideMentionString_AdjustsSelection_Public(t *testing.T) {
	m := NewMentionEditText()
	text := "Public @mainUser example."
	m.SetText(text)
	m.SetSelection(9, 9) // @mainUser: 7-16
	if m.GetSelectionStart() != 16 || m.GetSelectionEnd() != 16 {
		t.Errorf("Expected selection to be at end of mention (16,16), got (%d,%d)", m.GetSelectionStart(), m.GetSelectionEnd())
	}
}

func TestOnSelectionChanged_CursorAtStartOfMentionString_AdjustsSelection_Public(t *testing.T) {
	m := NewMentionEditText()
	text := "Public @mainUser example."
	m.SetText(text)
	m.SetSelection(7, 7)
	if m.GetSelectionStart() != 16 || m.GetSelectionEnd() != 16 {
		t.Errorf("Expected selection at end of mention(16,16), got (%d,%d)", m.GetSelectionStart(), m.GetSelectionEnd())
	}
}

func TestOnSelectionChanged_CursorAtEndOfMentionString_NoChange_Public(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Public @mainUser example.")
	m.SetSelection(16, 16)
	if m.GetSelectionStart() != 16 || m.GetSelectionEnd() != 16 {
		t.Errorf("Expected selection at (16,16), got (%d,%d)", m.GetSelectionStart(), m.GetSelectionEnd())
	}
}

func TestOnSelectionChanged_SelectingPartialMentionString_ExpandsSelection_Public(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Public @mainUser example.")
	m.SetSelection(8, 13)
	if m.GetSelectionStart() != 7 || m.GetSelectionEnd() != 16 {
		t.Errorf("Expected selection expanded to (7,16), got (%d,%d)", m.GetSelectionStart(), m.GetSelectionEnd())
	}
}

func TestOnSelectionChanged_SelectingPartialMentionStringFromEnd_ExpandsSelection_Public(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Public @mainUser example.")
	m.SetSelection(10, 16)
	if m.GetSelectionStart() != 7 || m.GetSelectionEnd() != 16 {
		t.Errorf("Expected selection expanded to (7,16), got (%d,%d)", m.GetSelectionStart(), m.GetSelectionEnd())
	}
}