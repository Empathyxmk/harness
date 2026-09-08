from src.renderEmail import render_email

def test_produces_expected_output_kitchen_sink():
    # Demo: cooked expected output as in sample
    kitchenSink = "<span style=\"font-family:sans-serif;font-size:15px;line-height:15px;color:#000\">Hello, world!</span>"
    actualOutput = render_email(lambda: kitchenSink)
    expectedOutput = '<!DOCTYPE html><html><body><span style="font-family:sans-serif;font-size:15px;line-height:15px;color:#000">Hello, world!</span></body></html>'
    assert actualOutput == expectedOutput

def test_warns_on_unsupported_property(monkeypatch):
    class DummyA:
        tag = "a"
    actualOutput = render_email(DummyA())
    expectedOutput = "<!DOCTYPE html><a></a>"
    assert actualOutput == expectedOutput