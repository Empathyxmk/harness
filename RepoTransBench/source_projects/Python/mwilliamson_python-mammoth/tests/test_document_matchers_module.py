import pytest
from mammoth import document_matchers as dm

def test_paragraph_and_table_and_run_matchers():
    para = dm.paragraph("id1", "name1", "num")
    assert para.style_id == "id1" and para.style_name == "name1"
    assert dm.ParagraphMatcher.element_type == "paragraph"

    run = dm.run("rid", "rname")
    assert run.style_id == "rid" and run.style_name == "rname"
    assert dm.RunMatcher.element_type == "run"

    table = dm.table("tid", "tname")
    assert table.style_id == "tid" and table.style_name == "tname"
    assert dm.TableMatcher.element_type == "table"

def test_inline_classes_types():
    assert dm.bold.element_type == "bold"
    assert dm.italic.element_type == "italic"
    assert dm.strikethrough.element_type == "strikethrough"
    assert dm.underline.element_type == "underline"
    assert dm.all_caps.element_type == "all_caps"
    assert dm.small_caps.element_type == "small_caps"
    assert dm.comment_reference.element_type == "comment_reference"

def test_highlight_matcher():
    h = dm.highlight("yellow")
    assert h.color == "yellow"
    assert dm.HighlightMatcher.element_type == "highlight"

def test_break_matchers():
    assert dm.line_break.break_type == "line"
    assert dm.page_break.break_type == "page"
    assert dm.column_break.break_type == "column"
    assert dm.BreakMatcher.element_type == "break"

def test_stringmatcher_equal_to_and_starts_with():
    eq = dm.equal_to("FooBar")
    st = dm.starts_with("abc")
    assert eq.matches("fooBAR") is True
    assert eq.matches("bar") is False
    assert st.matches("abcX") is True
    assert st.matches("nope") is False

def test_stringmatcher_repr():
    eq = dm.equal_to("Baz")
    assert "Baz" in repr(eq)