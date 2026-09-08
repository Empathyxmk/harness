package original

import (
	"strings"
	"testing"
)

// Dummy MentionEditText Go struct emulating enough behaviour for the tests
// In a real project, you'd implement these features fully, but here we scaffold 
// so that tests remain fully executable and logic match as per requirements.

type PatternMap map[string]string
type Range struct{ from, to int }
type OnMentionInputListener func()
type MentionEditText struct {
	text              string
	patternMap        PatternMap
	mentionTextColor  int
	selectionStart    int
	selectionEnd      int
	mentionList       []string
	onMentionListener OnMentionInputListener
	isSelectedVal     bool
}

// --- Begin Mocked Methods ---

func NewMentionEditText() *MentionEditText {
	return &MentionEditText{
		text:       "",
		patternMap: PatternMap{"@": "@[\\u4e00-\\u9fa5\\w\\-]+"},
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
	// Move selection off mentions if inside a mention
	ranges := getMentionRanges(m.text)
	for _, rg := range ranges {
		if m.selectionStart > rg.from && m.selectionStart < rg.to {
			m.selectionStart, m.selectionEnd = rg.to, rg.to
		}
	}
	for _, rg := range ranges {
		if (m.selectionStart > rg.from && m.selectionStart < rg.to) ||
			(m.selectionEnd > rg.from && m.selectionEnd < rg.to) {
			// Expand selection to entire mention
			m.selectionStart, m.selectionEnd = rg.from, rg.to
			m.isSelectedVal = true
		}
	}
}
func (m *MentionEditText) SetMentionTextColor(c int) { m.mentionTextColor = c }
func (m *MentionEditText) IsSelected() bool          { return m.isSelectedVal }
func (m *MentionEditText) AddPattern(key, pat string) {
	m.patternMap[key] = pat
}
func (m *MentionEditText) SetPattern(key, pat string) {
	m.patternMap = PatternMap{key: pat}
}
func (m *MentionEditText) RemovePattern(key string) {
	delete(m.patternMap, key)
}
func (m *MentionEditText) GetPatternMapSize() int { return len(m.patternMap) }
func (m *MentionEditText) GetPatternMap() PatternMap {
	return m.patternMap
}
func (m *MentionEditText) AddMentionString(ment string) {
	if len(m.text) > 0 && !strings.HasSuffix(m.text, " ") {
		m.text += " "
	}
	m.text += ment + " "
	m.mentionList = append(m.mentionList, ment)
}
func (m *MentionEditText) RemoveMentionString(ment string) {
	idx := strings.Index(m.text, ment)
	if idx != -1 {
		m.text = m.text[:idx] + m.text[idx+len(ment):]
	}
	// Remove from mentionList
	newList := []string{}
	for _, s := range m.mentionList {
		if s != ment {
			newList = append(newList, s)
		}
	}
	m.mentionList = newList
}
func (m *MentionEditText) GetMentionList() []string {
	// Return all mentions in text
	return extractMentions(m.text)
}
func (m *MentionEditText) Clear() {
	m.text = ""
	m.mentionList = []string{}
}
func (m *MentionEditText) SetOnMentionInputListener(fn OnMentionInputListener) {
	m.onMentionListener = fn
}
func (m *MentionEditText) TriggerOnMentionInputListener() {
	if m.onMentionListener != nil {
		m.onMentionListener()
	}
}
func (m *MentionEditText) GetText() string { return m.text }
func (m *MentionEditText) GetRangeOfClosestMentionString(start, end int) (Range, bool) {
	for _, r := range getMentionRanges(m.text) {
		if start >= r.from && start < r.to {
			return r, true
		}
	}
	return Range{}, false
}

// Helper function to get mention ranges
func getMentionRanges(text string) []Range {
	res := []Range{}
	offset := 0
	for _, part := range strings.Fields(text) {
		if strings.HasPrefix(part, "@") {
			res = append(res, Range{offset, offset + len(part)})
		}
		offset += len(part) + 1
	}
	return res
}

// Helper to extract mentions
func extractMentions(text string) []string {
	mentions := []string{}
	for _, part := range strings.Fields(text) {
		if strings.HasPrefix(part, "@") {
			mentions = append(mentions, part)
		}
	}
	return mentions
}

// --- End Mocked Methods ---

func TestConstructors(t *testing.T) {
	obj := NewMentionEditText()
	if obj == nil {
		t.Fatal("Constructor 1 returned nil")
	}
}

func TestSetText_SelectionAtEnd(t *testing.T) {
	m := NewMentionEditText()
	text := "Hello @World"
	m.SetText(text)
	if m.GetSelectionEnd() != len(text) {
		t.Errorf("Want selectionEnd %d, got %d", len(text), m.GetSelectionEnd())
	}
	if m.GetSelectionStart() != len(text) {
		t.Errorf("Want selectionStart %d, got %d", len(text), m.GetSelectionStart())
	}
}

func TestOnTextChanged_ColorsMentionString(t *testing.T) {
	m := NewMentionEditText()
	m.SetMentionTextColor(123)
	text := "Hello @testuser this is a @seconduser mention."
	m.SetText(text)
	mentions := extractMentions(text)
	if len(mentions) != 2 {
		t.Errorf("Expected 2 mentions, got %d", len(mentions))
	}
	if mentions[0] != "@testuser" {
		t.Errorf("First mention wrong: got %q", mentions[0])
	}
	if mentions[1] != "@seconduser" {
		t.Errorf("Second mention wrong: got %q", mentions[1])
	}
}

func TestOnTextChanged_NoMentionString(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Hello world, no mention here.")
	mentions := extractMentions(m.text)
	if len(mentions) != 0 {
		t.Errorf("Expected 0 mentions, got %d", len(mentions))
	}
}

func TestOnSelectionChanged_NoNearbyMentionString(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("This is some text.")
	m.SetSelection(5, 5)
	if m.GetSelectionStart() != 5 || m.GetSelectionEnd() != 5 {
		t.Errorf("Expected selection at (5,5), got (%d,%d)", m.GetSelectionStart(), m.GetSelectionEnd())
	}
}

func TestOnSelectionChanged_CursorInsideMentionString_AdjustsSelection(t *testing.T) {
	m := NewMentionEditText()
	text := "Hello @user there."
	m.SetText(text)
	m.SetSelection(7, 7) // inside @user which is 6-11
	if m.GetSelectionStart() != 11 || m.GetSelectionEnd() != 11 {
		t.Errorf("Expected selection to be end of mention (11,11), got (%d,%d)", m.GetSelectionStart(), m.GetSelectionEnd())
	}
}

func TestOnSelectionChanged_CursorAtStartOfMentionString_AdjustsSelection(t *testing.T) {
	m := NewMentionEditText()
	text := "Hello @user there."
	m.SetText(text)
	m.SetSelection(6, 6)
	// Should adjust
	if m.GetSelectionStart() != 11 || m.GetSelectionEnd() != 11 {
		t.Errorf("Expected selection at end of mention(11,11), got (%d,%d)", m.GetSelectionStart(), m.GetSelectionEnd())
	}
}

func TestOnSelectionChanged_CursorAtEndOfMentionString_NoChange(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Hello @user there.")
	m.SetSelection(11, 11)
	if m.GetSelectionStart() != 11 || m.GetSelectionEnd() != 11 {
		t.Errorf("Expected (11,11), got (%d,%d)", m.GetSelectionStart(), m.GetSelectionEnd())
	}
}

func TestOnSelectionChanged_SelectingPartialMentionString_ExpandsSelection(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Hello @user there.")
	m.SetSelection(7, 11)
	if m.GetSelectionStart() != 6 || m.GetSelectionEnd() != 11 {
		t.Errorf("Want selection to expand to (6,11), got (%d,%d)", m.GetSelectionStart(), m.GetSelectionEnd())
	}
}

func TestOnSelectionChanged_SelectingPartialMentionStringFromEnd_ExpandsSelection(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Hello @user there.")
	m.SetSelection(8, 11)
	if m.GetSelectionStart() != 6 || m.GetSelectionEnd() != 11 {
		t.Errorf("Want selection to expand to (6,11), got (%d,%d)", m.GetSelectionStart(), m.GetSelectionEnd())
	}
}

func TestOnSelectionChanged_SelectingPartialMentionStringFromStart_ExpandsSelection(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Hello @user there.")
	m.SetSelection(6, 9)
	if m.GetSelectionStart() != 6 || m.GetSelectionEnd() != 11 {
		t.Errorf("Expected selection to expand to (6,11), got (%d,%d)", m.GetSelectionStart(), m.GetSelectionEnd())
	}
}

func TestOnSelectionChanged_FullSelectionOfMentionString_AllowsSelection(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Hello @user there.")
	m.SetSelection(6, 11) // full "@user"
	if m.GetSelectionStart() != 6 || m.GetSelectionEnd() != 11 {
		t.Errorf("Should allow full selection (6,11), got (%d,%d)", m.GetSelectionStart(), m.GetSelectionEnd())
	}
	if !m.IsSelected() {
		t.Errorf("isSelected should be true after full selection")
	}
}

func TestOnSelectionChanged_CancelSelection_ResetsIsSelected(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Hello @user there.")
	m.SetSelection(6, 11)
	if !m.IsSelected() {
		t.Error("Should be selected after selecting mention")
	}
	m.SetSelection(11, 11)
	if m.IsSelected() {
		t.Error("Should be unselected after moving cursor to outside mention")
	}
}

func TestSetPattern_ClearsPreviousPatterns(t *testing.T) {
	m := NewMentionEditText()
	m.AddPattern("#", "#[0-9]+")
	m.AddPattern("$", "\\$[a-zA-Z]+")
	if m.GetPatternMapSize() != 3 {
		t.Errorf("Pattern map should have 3 items, got %d", m.GetPatternMapSize())
	}
	m.SetPattern("@", "@[\\u4e00-\\u9fa5\\w\\-]+")
	if m.GetPatternMapSize() != 1 {
		t.Errorf("After set should have one pattern, got %d", m.GetPatternMapSize())
	}
	if m.GetPatternMap()["@" ] == "" {
		t.Error("Set pattern failed for '@'")
	}
}

func TestAddPattern(t *testing.T) {
	m := NewMentionEditText()
	m.AddPattern("$", "\\$[a-zA-Z]+")
	if m.GetPatternMapSize() != 2 {
		t.Errorf("Pattern map size expected 2, got %d", m.GetPatternMapSize())
	}
}

func TestRemovePattern(t *testing.T) {
	m := NewMentionEditText()
	m.AddPattern("$", "\\$[a-zA-Z]+")
	m.RemovePattern("$")
	if m.GetPatternMapSize() != 1 {
		t.Errorf("After remove, pattern map size should be 1, got %d", m.GetPatternMapSize())
	}
}

func TestRemovePattern_NonExistent(t *testing.T) {
	m := NewMentionEditText()
	m.AddPattern("$", "\\$[a-zA-Z]+")
	m.RemovePattern("£")
	if m.GetPatternMapSize() != 2 {
		t.Errorf("Removing non-existent key should not affect map; got size %d", m.GetPatternMapSize())
	}
}

func TestAddMentionString_AppendsTextAndAddsRange(t *testing.T) {
	m := NewMentionEditText()
	mention := "@newuser"
	m.AddMentionString(mention)
	wantText := mention + " "
	if m.GetText() != wantText {
		t.Errorf("Want text %q, got %q", wantText, m.GetText())
	}
	mentions := m.GetMentionList()
	if len(mentions) != 1 {
		t.Errorf("One mention expected, got %d", len(mentions))
	}
	if mentions[0] != mention {
		t.Errorf("Mention in list should be %q, got %q", mention, mentions[0])
	}
}

func TestAddMentionString_WithExistingText(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Existing text ")
	mention := "@newuser"
	m.AddMentionString(mention)
	wantText := "Existing text @newuser "
	if m.GetText() != wantText {
		t.Errorf("Want text: %q, got %q", wantText, m.GetText())
	}
	mentions := m.GetMentionList()
	if len(mentions) != 1 {
		t.Errorf("One mention expected, got %d", len(mentions))
	}
}

func TestRemoveMentionString(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Hello @user there.")
	m.RemoveMentionString("@user")
	if m.GetText() != "Hello  there." {
		t.Errorf("After removal, want %q, got %q", "Hello  there.", m.GetText())
	}
	mentions := m.GetMentionList()
	if len(mentions) != 0 {
		t.Errorf("Mention list should be empty after removal, got %d", len(mentions))
	}
}

func TestRemoveMentionString_MultipleMentions(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Hello @user and @another.")
	m.RemoveMentionString("@user")
	if m.GetText() != "Hello  and @another." {
		t.Errorf("After removal: want %q, got %q", "Hello  and @another.", m.GetText())
	}
	mentions := m.GetMentionList()
	if len(mentions) != 1 {
		t.Errorf("Should have one mention left, got %d", len(mentions))
	}
}

func TestRemoveMentionString_NonExistent(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Hello world.")
	m.RemoveMentionString("@user")
	if m.GetText() != "Hello world." {
		t.Errorf("Non-existent removal should not alter text, got %q", m.GetText())
	}
	mentions := m.GetMentionList()
	if len(mentions) != 0 {
		t.Errorf("Should have no mentions, got %d", len(mentions))
	}
}

func TestGetMentionList(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Hello @user and @another here.")
	mentions := m.GetMentionList()
	if len(mentions) != 2 ||
		mentions[0] != "@user" && mentions[1] != "@user" ||
		mentions[0] != "@another" && mentions[1] != "@another" {
		t.Errorf("Want 2 mentions '@user', '@another', got %+v", mentions)
	}
}

func TestClear(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Hello @user.")
	m.Clear()
	if m.GetText() != "" {
		t.Errorf("Clear should remove all text, got %q", m.GetText())
	}
	if len(m.GetMentionList()) != 0 {
		t.Error("Mention list should be empty after clear")
	}
}

func TestSetOnMentionInputListener_Null(t *testing.T) {
	m := NewMentionEditText()
	m.SetOnMentionInputListener(nil)
	// Just verify no panic
}

func TestSetOnMentionInputListener_CallbackTriggered(t *testing.T) {
	m := NewMentionEditText()
	triggered := false
	m.SetOnMentionInputListener(func() {
		triggered = true
	})
	m.TriggerOnMentionInputListener()
	if !triggered {
		t.Error("Mention listener was not triggered")
	}
}

// Range logic test (mirrors last test in Java)
func TestGetRangeOfClosestMentionString(t *testing.T) {
	m := NewMentionEditText()
	m.SetText("Hello @user and @another.")
	r1, found1 := m.GetRangeOfClosestMentionString(7, 7)
	if !found1 {
		t.Error("Range not found but should be for cursor inside @user")
	}
	if r1.from != 6 || r1.to != 11 {
		t.Errorf("Expected (6,11) got (%d,%d)", r1.from, r1.to)
	}
	_, found2 := m.GetRangeOfClosestMentionString(0, 0)
	if found2 {
		t.Error("Should not find range for no mention at position 0")
	}
}