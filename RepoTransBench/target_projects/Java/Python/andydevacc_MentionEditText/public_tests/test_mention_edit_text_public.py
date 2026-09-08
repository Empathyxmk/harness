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
    COLOR_RED = 0xFFFF0000

    def __init__(self, context=None, attrs=None, defStyleAttr=0):
        self.text = ""
        self.selection = (0, 0)
        self.mention_text_color = self.COLOR_RED
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


def test_Constructors_Public():
    m1 = MockMentionEditText()
    m2 = MockMentionEditText(None)
    m3 = MockMentionEditText(None, None, 0)
    assert m1 is not None
    assert m2 is not None
    assert m3 is not None

def test_SetText_SelectionAtEnd_Public():
    met = MockMentionEditText()
    text = "Test @ExampleUser"
    met.setText(text)
    assert met.getSelectionEnd() == len(text)
    assert met.getSelectionStart() == len(text)

def test_OnTextChanged_ColorsMentionString_Public():
    met = MockMentionEditText()
    met.setMentionTextColor(MockMentionEditText.COLOR_RED)
    text = "Greetings @alphaTest and @bravoTester!"
    met.setText(text)
    spans = []
    for m in met.mentions:
        spans.append(MockForegroundColorSpan(MockMentionEditText.COLOR_RED, m['from'], m['to']))
    assert len(spans) == 2
    mention1 = met.text[spans[0].get_start():spans[0].get_end()]
    assert mention1 == "@alphaTest"
    assert spans[0].getForegroundColor() == MockMentionEditText.COLOR_RED
    mention2 = met.text[spans[1].get_start():spans[1].get_end()]
    assert mention2 == "@bravoTester"
    assert spans[1].getForegroundColor() == MockMentionEditText.COLOR_RED

def test_OnTextChanged_NoMentionString_Public():
    met = MockMentionEditText()
    met.setText("Nothing special here, just text.")
    assert len(met.mentions) == 0

def test_OnSelectionChanged_NoNearbyMentionString_Public():
    met = MockMentionEditText()
    met.setText("Public input string.")
    met.setSelection(8,8)
    assert met.getSelectionStart() == 8
    assert met.getSelectionEnd() == 8

def test_OnSelectionChanged_CursorInsideMentionString_AdjustsSelection_Public():
    met = MockMentionEditText()
    text = "Public @mainUser example."
    met.setText(text)
    met.setSelection(9,9)
    assert met.getSelectionStart() == 16
    assert met.getSelectionEnd() == 16

def test_OnSelectionChanged_CursorAtStartOfMentionString_AdjustsSelection_Public():
    met = MockMentionEditText()
    text = "Public @mainUser example."
    met.setText(text)
    met.setSelection(7,7)
    assert met.getSelectionStart() == 16
    assert met.getSelectionEnd() == 16

def test_OnSelectionChanged_CursorAtEndOfMentionString_NoChange_Public():
    met = MockMentionEditText()
    text = "Public @mainUser example."
    met.setText(text)
    met.setSelection(16,16)
    assert met.getSelectionStart() == 16
    assert met.getSelectionEnd() == 16

def test_OnSelectionChanged_SelectingPartialMentionString_ExpandsSelection_Public():
    met = MockMentionEditText()
    text = "Public @mainUser example."
    met.setText(text)
    met.setSelection(8,13)
    assert met.getSelectionStart() == 7
    assert met.getSelectionEnd() == 16

def test_OnSelectionChanged_SelectingPartialMentionStringFromEnd_ExpandsSelection_Public():
    met = MockMentionEditText()
    text = "Public @mainUser example."
    met.setText(text)
    met.setSelection(10,16)
    assert met.getSelectionStart() == 7
    assert met.getSelectionEnd() == 16