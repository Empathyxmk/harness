import ast
from pathlib import Path

def test_lint_session_exists_and_is_def():
    # Parse the noxfile as text and look for the "lint" session
    noxfile_path = Path(__file__).parent.parent / "noxfile.py"
    src = noxfile_path.read_text(encoding="utf-8")
    tree = ast.parse(src, filename="noxfile.py")
    # Find the "lint" function definition
    lint_func = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "lint":
            lint_func = node
            break
    assert lint_func is not None, "lint session must exist"
    assert lint_func.name == "lint"
    # Public: check that it takes at least one parameter
    assert len(lint_func.args.args) >= 1

def test_lint_session_decorator_includes_session():
    # Make sure @nox.session is present
    noxfile_path = Path(__file__).parent.parent / "noxfile.py"
    src = noxfile_path.read_text(encoding="utf-8")
    tree = ast.parse(src, filename="noxfile.py")
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "lint":
            found = any( 
                (
                    (isinstance(deco, ast.Attribute) and deco.attr == "session")
                    or
                    (isinstance(deco, ast.Call) and getattr(deco.func, "attr", None) == "session")
                )
                for deco in node.decorator_list
            )
            assert found, "lint should be decorated with @nox.session"

def test_lint_session_calls_run_with_specific_args():
    # The lint function should call session.run with "flake8" or "pytest" or "mypy"
    noxfile_path = Path(__file__).parent.parent / "noxfile.py"
    src = noxfile_path.read_text(encoding="utf-8")
    tree = ast.parse(src, filename="noxfile.py")
    words = {"flake8", "pytest", "mypy"}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "lint":
            for st in ast.walk(node):
                if isinstance(st, ast.Call):
                    if hasattr(st.func, "attr") and st.func.attr == "run":
                        if st.args:
                            val = None
                            if isinstance(st.args[0], ast.Constant):
                                val = st.args[0].value
                            elif isinstance(st.args[0], ast.Str):
                                val = st.args[0].s
                            if val and val in words:
                                return
    assert False, "Should call session.run with flake8 or pytest or mypy"