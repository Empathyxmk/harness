import pytest

class MockForegroundColorSpan:
    def __init__(self, color, start, end):
        self._color = color
        self._start = start
        self._end = end

    def getForegroundColor(self):
        return self._color

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end


class MockMentionEditText:
    COLOR_BLUE = 0xFF0000FF

    def __init__(self, context=None, attrs=None, defStyleAttr=0):
        self.text = ""
        self.selection = (0, 0)
        self.mention_text_color = self.COLOR_BLUE
        self.pattern_map = {"@": r"@\w+"}
        self.mentions = []
        self.is_selected = False
        self.listener = None

    def setText(self, txt):
        self.text = txt
        self._update_mentions()
        self.selection = (len(txt), len(txt))
        self.is_selected = False if self.selection[0] == self.selection[1] else True

    def setMentionTextColor(self, color):
        self.mention_text_color = color

    def getText(self):
        return self.text

    def getSelectionStart(self):
        return self.selection[0]

    def getSelectionEnd(self):
        return self.selection[1]

    def setSelection(self, start, end=None):
        if end is None:
            end = start
        # Simulate Java logic for changing selection
        # If selection only inside a mention, expand,
        # If at the end of mention, leave as is.
        for m in self.mentions:
            m_s, m_e = m['from'], m['to']
            if (start > m_s and start < m_e) or (end > m_s and end < m_e):
                self.selection = (m_e, m_e)
                self.is_selected = False
                return
            if (start == m_s and end != m_e) or (end == m_e and start != m_s):
                self.selection = (m_s, m_e)
                self.is_selected = True
                return
            if start == m_e and end == m_e:
                self.selection = (m_e, m_e)
                self.is_selected = False
                return
            if start == m_s and end == m_e:
                self.selection = (m_s, m_e)
                self.is_selected = True
                return
        self.selection = (start, end)
        self.is_selected = start != end

    def isSelected(self):
        return self.is_selected

    def setOnMentionInputListener(self, listener):
        self.listener = listener

    def _update_mentions(self):
        import re
        self.mentions = []
        pat = self.pattern_map.get("@", r"@\w+")
        for match in re.finditer(pat, self.text):
            self.mentions.append({'from': match.start(), 'to': match.end(), 'text': match.group()})

    def addPattern(self, key, regex):
        self.pattern_map[key] = regex

    def setPattern(self, key, regex):
        self.pattern_map = {key: regex}

    def getPatternMapSize(self):
        return len(self.pattern_map)

    def getPatternMap(self):
        return self.pattern_map

    def removePattern(self, key):
        if key in self.pattern_map:
            del self.pattern_map[key]

    def addMentionString(self, mention):
        if self.text and not self.text.endswith(" "):
            self.text += " "
        start = len(self.text)
        self.text += mention + " "
        self.mentions.append({'from': start, 'to': start + len(mention), 'text': mention})
        self.selection = (len(self.text), len(self.text))

    def removeMentionString(self, mention):
        import re
        found = False
        for m in self.mentions:
            if m['text'] == mention and not found:
                new_txt = self.text[:m['from']] + self.text[m['to']:]
                # Remove extra space before/after
                before = new_txt[:m['from']]
                after = new_txt[m['from']:]
                if before and before[-1] == " " and after and after[0] == " ":
                    new_txt = new_txt[:m['from']] + new_txt[m['from']+1:]
                self.text = new_txt
                found = True
                self.selection = (m['from'], m['from'])
                break
        self._update_mentions()

    def getMentionList(self):
        return [m['text'] for m in self.mentions]

    def clear(self):
        self.text = ""
        self.mentions = []
        self.selection = (0, 0)

    def onCreateInputConnection(self, editor_info=None):
        return self

    # Simulate HackInputConnection logic for deletion
    def deleteSurroundingText(self, beforeLength, afterLength):
        if beforeLength == 1 and self.selection[0] == self.selection[1]:
            cur = self.selection[0]
            for m in self.mentions:
                if cur == m['to']:
                    # delete mention
                    self.text = self.text[:m['from']] + self.text[m['to']:]
                    self.selection = (m['from'], m['from'])
                    self._update_mentions()
                    return
                if cur > m['from'] and cur < m['to']:
                    self.text = self.text[:m['from']] + self.text[m['to']:]
                    self.selection = (m['from'], m['from'])
                    self._update_mentions()
                    return
        # Normal text deletion
        start = self.selection[0]
        if beforeLength and start - beforeLength >= 0:
            self.text = self.text[:start - beforeLength] + self.text[start:]
            self.selection = (start - beforeLength, start - beforeLength)

    def sendKeyEvent(self, event):
        if hasattr(event, "keycode") and event.keycode == "del":
            self.deleteSurroundingText(1, 0)
        else:
            # Just regular typing; not handled here
            pass

    # For public API compatibility:
    class Range:
        def __init__(self, from_idx, to_idx):
            self.from_ = from_idx
            self.to = to_idx

    def getRangeOfClosestMentionString(self, start, end):
        for m in self.mentions:
            if start >= m['from'] and start <= m['to']:
                return self.Range(m['from'], m['to'])
            if end >= m['from'] and end <= m['to']:
                return self.Range(m['from'], m['to'])
        return None



def test_Constructors():
    m1 = MockMentionEditText()
    m2 = MockMentionEditText(None)
    m3 = MockMentionEditText(None, None, 0)
    assert m1 is not None
    assert m2 is not None
    assert m3 is not None

def test_SetText_SelectionAtEnd():
    met = MockMentionEditText()
    text = "Hello @World"
    met.setText(text)
    assert met.getSelectionEnd() == len(text)
    assert met.getSelectionStart() == len(text)

def test_OnTextChanged_ColorsMentionString():
    met = MockMentionEditText()
    met.setMentionTextColor(MockMentionEditText.COLOR_BLUE)
    text = "Hello @testuser this is a @seconduser mention."
    met.setText(text)
    # Emulate color spans
    spans = []
    for m in met.mentions:
        spans.append(MockForegroundColorSpan(MockMentionEditText.COLOR_BLUE, m['from'], m['to']))
    assert len(spans) == 2
    mention1 = met.text[spans[0].get_start():spans[0].get_end()]
    assert mention1 == "@testuser"
    assert spans[0].getForegroundColor() == MockMentionEditText.COLOR_BLUE
    mention2 = met.text[spans[1].get_start():spans[1].get_end()]
    assert mention2 == "@seconduser"
    assert spans[1].getForegroundColor() == MockMentionEditText.COLOR_BLUE

def test_OnTextChanged_NoMentionString():
    met = MockMentionEditText()
    met.setText("Hello world, no mention here.")
    assert len(met.mentions) == 0

def test_OnSelectionChanged_NoNearbyMentionString():
    met = MockMentionEditText()
    met.setText("This is some text.")
    met.setSelection(5, 5)
    assert met.getSelectionStart() == 5
    assert met.getSelectionEnd() == 5

def test_OnSelectionChanged_CursorInsideMentionString_AdjustsSelection():
    met = MockMentionEditText()
    text = "Hello @user there."
    met.setText(text)
    met.setSelection(7,7)
    assert met.getSelectionStart() == 11
    assert met.getSelectionEnd() == 11

def test_OnSelectionChanged_CursorAtStartOfMentionString_AdjustsSelection():
    met = MockMentionEditText()
    text = "Hello @user there."
    met.setText(text)
    met.setSelection(6,6)
    assert met.getSelectionStart() == 11
    assert met.getSelectionEnd() == 11

def test_OnSelectionChanged_CursorAtEndOfMentionString_NoChange():
    met = MockMentionEditText()
    text = "Hello @user there."
    met.setText(text)
    met.setSelection(11,11)
    assert met.getSelectionStart() == 11
    assert met.getSelectionEnd() == 11

def test_OnSelectionChanged_SelectingPartialMentionString_ExpandsSelection():
    met = MockMentionEditText()
    text = "Hello @user there."
    met.setText(text)
    met.setSelection(7,11)
    assert met.getSelectionStart() == 6
    assert met.getSelectionEnd() == 11

def test_OnSelectionChanged_SelectingPartialMentionStringFromEnd_ExpandsSelection():
    met = MockMentionEditText()
    text = "Hello @user there."
    met.setText(text)
    met.setSelection(8,11)
    assert met.getSelectionStart() == 6
    assert met.getSelectionEnd() == 11

def test_OnSelectionChanged_SelectingPartialMentionStringFromStart_ExpandsSelection():
    met = MockMentionEditText()
    text = "Hello @user there."
    met.setText(text)
    met.setSelection(6,9)
    assert met.getSelectionStart() == 6
    assert met.getSelectionEnd() == 11

def test_OnSelectionChanged_FullSelectionOfMentionString_AllowsSelection():
    met = MockMentionEditText()
    text = "Hello @user there."
    met.setText(text)
    met.setSelection(6,11)
    assert met.getSelectionStart() == 6
    assert met.getSelectionEnd() == 11
    assert met.isSelected()

def test_OnSelectionChanged_CancelSelection_ResetsIsSelected():
    met = MockMentionEditText()
    text = "Hello @user there."
    met.setText(text)
    met.setSelection(6,11)
    assert met.isSelected()
    met.setSelection(11,11)
    assert not met.isSelected()

def test_SetPattern_ClearsPreviousPatterns():
    met = MockMentionEditText()
    met.addPattern("#", "#[0-9]+")
    met.addPattern("$", r"\$[a-zA-Z]+")
    assert met.getPatternMapSize() == 3
    met.setPattern("@", r"@[\u4e00-\u9fa5\w\-]+")
    assert met.getPatternMapSize() == 1
    assert met.getPatternMap().get("@") is not None

def test_AddPattern():
    met = MockMentionEditText()
    met.addPattern("$", r"\$[a-zA-Z]+")
    assert met.getPatternMapSize() == 2
    assert met.getPatternMap().get("$") is not None

def test_RemovePattern():
    met = MockMentionEditText()
    met.addPattern("$", r"\$[a-zA-Z]+")
    met.removePattern("$")
    assert met.getPatternMapSize() == 1
    assert met.getPatternMap().get("$") is None

def test_RemovePattern_NonExistent():
    met = MockMentionEditText()
    met.addPattern("$", r"\$[a-zA-Z]+")
    met.removePattern("£")
    assert met.getPatternMapSize() == 2

def test_AddMentionString_AppendsTextAndAddsRange():
    met = MockMentionEditText()
    mention = "@newuser"
    met.addMentionString(mention)
    assert met.getText() == mention + " "
    assert len(met.mentions) == 1
    assert met.mentions[0]['from'] == 0
    assert met.mentions[0]['to'] == len(mention)

def test_AddMentionString_WithExistingText():
    met = MockMentionEditText()
    met.setText("Existing text ")
    mention = "@newuser"
    met.addMentionString(mention)
    assert met.getText() == "Existing text @newuser "
    assert len(met.mentions) == 1
    assert met.mentions[0]['from'] == len("Existing text ")
    assert met.mentions[0]['to'] == len("Existing text ") + len(mention)

def test_RemoveMentionString():
    met = MockMentionEditText()
    met.setText("Hello @user there.")
    met.removeMentionString("@user")
    assert met.getText().strip() == "Hello  there."
    assert len(met.mentions) == 0

def test_RemoveMentionString_MultipleMentions():
    met = MockMentionEditText()
    met.setText("Hello @user and @another.")
    met.removeMentionString("@user")
    assert "@another" in met.getText()
    assert len(met.mentions) == 1
    m = met.mentions[0]
    assert met.text[m['from']:m['to']] == "@another"

def test_RemoveMentionString_NonExistent():
    met = MockMentionEditText()
    met.setText("Hello world.")
    met.removeMentionString("@user")
    assert met.getText() == "Hello world."
    assert len(met.mentions) == 0

def test_GetMentionList():
    met = MockMentionEditText()
    met.setText("Hello @user and @another here.")
    mentions = met.getMentionList()
    assert len(mentions) == 2
    assert "@user" in mentions
    assert "@another" in mentions

def test_Clear():
    met = MockMentionEditText()
    met.setText("Hello @user.")
    met.clear()
    assert met.getText() == ""
    assert not met.getMentionList()

def test_SetOnMentionInputListener_Null():
    met = MockMentionEditText()
    met.setOnMentionInputListener(None)
    # No exceptions

def test_HackInputConnection_DeleteSurroundingText_DeleteMention():
    met = MockMentionEditText()
    met.setText("text @user")
    met.setSelection(10,10)
    met.deleteSurroundingText(1,0)  # delete '@user'
    assert met.getText() == "text "
    assert len(met.mentions) == 0
    assert met.getSelectionStart() == 5
    assert met.getSelectionEnd() == 5

def test_HackInputConnection_DeleteSurroundingText_DeletePartialMention_ShouldDeleteFull():
    met = MockMentionEditText()
    met.setText("text @user")
    met.setSelection(8,8) # inside '@user'
    met.deleteSurroundingText(1,0)
    assert met.getText() == "text "
    assert len(met.mentions) == 0
    assert met.getSelectionStart() == 5

def test_HackInputConnection_DeleteSurroundingText_DeleteNormalText():
    met = MockMentionEditText()
    met.setText("text user")
    met.setSelection(9,9)
    met.deleteSurroundingText(1,0)
    assert met.getText() == "text use"
    assert met.getSelectionStart() == 8
    assert met.getSelectionEnd() == 8

def test_HackInputConnection_DeleteSurroundingText_SelectionAcrossMention():
    met = MockMentionEditText()
    met.setText("before @user after")
    met.setSelection(4,11)
    # emulate deletion of selected text (like deleteSurroundingText(0,0))
    # Should delete selection 4:11
    met.text = met.text[:4] + met.text[11:]
    met._update_mentions()
    assert met.getText() == "bfor after"
    assert len(met.mentions) == 0

def test_HackInputConnection_SendKeyEvent_DeleteAction():
    met = MockMentionEditText()
    met.setText("text @user")
    met.setSelection(10,10)
    class Event:
        keycode = "del"
    met.sendKeyEvent(Event())
    assert met.getText() == "text "
    assert len(met.mentions) == 0
    assert met.getSelectionStart() == 5
    assert met.getSelectionEnd() == 5

def test_HackInputConnection_SendKeyEvent_OtherAction():
    met = MockMentionEditText()
    met.setText("text @user")
    met.setSelection(10,10)
    class Event:
        keycode = "A"
    met.sendKeyEvent(Event())
    assert met.getText() == "text @user"

def test_HackInputConnection_SendKeyEvent_MultipleDeletions():
    met = MockMentionEditText()
    met.setText("first @user second @test third")
    met.setSelection(17,17) # after @test
    class Event:
        keycode = "del"
    # First deletion, delete @test
    met.sendKeyEvent(Event())
    assert met.getText() == "first @user second  third"
    assert len(met.mentions) == 1
    assert met.getSelectionStart() == 16
    assert met.getSelectionEnd() == 16
    # Second deletion, delete space
    met.sendKeyEvent(Event())
    assert met.getText() == "first @user second third"
    assert met.getSelectionStart() == 15
    assert met.getSelectionEnd() == 15
    # Third deletion, delete 'd'
    met.sendKeyEvent(Event())
    assert met.getText() == "first @user second thir"
    assert met.getSelectionStart() == 14
    assert met.getSelectionEnd() == 14

def test_GetRangeOfClosestMentionString():
    met = MockMentionEditText()
    met.setText("Hello @user and @another.")
    # Cursor within '@user'
    r1 = met.getRangeOfClosestMentionString(7,7)
    assert r1 is not None and met.text[r1.from_:r1.to] == "@user"
    # Cursor within '@another'
    r2 = met.getRangeOfClosestMentionString(17,17)
    assert r2 is not None and met.text[r2.from_:r2.to] == "@another"
    # Cursor not in mention
    r3 = met.getRangeOfClosestMentionString(0,0)
    assert r3 is None