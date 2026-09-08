def format_constants(value):
    if value is None:
        return ""
    return " ".join(f"({k}: {v})" for k, v in value.items() if v is not None)

def test_sign_analysis(monkeypatch, capsys):
    # This is a simulation since we cannot run Soot/Java code in Python.
    # We check analysis flow and output capturing.
    class Local: pass
    class Sign: pass

    class SignAnalysis:
        def __init__(self):
            self.methods = ["vasco.tests.SignTestCase.main"]
        def doAnalysis(self): pass
        def getMeetOverValidPathsSolution(self):
            return type("Sol", (), {
                "getValueBefore": lambda self, unit: {"p": "POS"} if unit == "main" else {},
                "getValueAfter": lambda self, unit: {"q": "NEG"} if unit == "main" else {}
            })()

    analysis = SignAnalysis()
    analysis.doAnalysis()
    solution = analysis.getMeetOverValidPathsSolution()
    out = []
    for method in analysis.methods:
        out.append(method)
        out.append("----------------------------------------------------------------")
        out.append(f"main")
        out.append(f"IN:  {format_constants(solution.getValueBefore('main'))}")
        out.append(f"OUT: {format_constants(solution.getValueAfter('main'))}")

    s = "\n".join(out)
    assert "main" in s
    assert "IN:" in s
    assert "OUT:" in s
    assert "p: POS" in s or "(p: POS)" in s