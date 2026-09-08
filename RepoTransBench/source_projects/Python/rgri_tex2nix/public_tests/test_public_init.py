import sys
import os
import importlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tex2nix")))

tex2nix = importlib.import_module("__init__")

def get_version():
    if hasattr(tex2nix, "__version__"):
        return tex2nix.__version__
    version = None
    init_path = os.path.join(os.path.dirname(__file__), "..", "tex2nix", "__init__.py")
    with open(init_path) as f:
        for line in f:
            if "__version__" in line and "=" in line:
                version = line.split("=")[-1].strip().replace('"', '').replace("'", "")
                break
    return version

def test_tex2nix_version():
    version = get_version()
    if version is not None:
        assert isinstance(version, str)
        assert len(version.split(".")) == 3

def test_main_entry_returns_none(monkeypatch):
    import tempfile
    if hasattr(tex2nix, "main"):
        import inspect
        main_obj = tex2nix.main
        sig = inspect.signature(main_obj)
        import io
        import contextlib

        # Patch get_nix_packages to return a set (not list!) to match code expectations in intersection
        monkeypatch.setattr(tex2nix, "get_nix_packages", lambda: set([
            "standalone", "publicpackage", "fancyhdr", "longtable", "pgfplots", "subcaption",
            "caption", "blindtext", "geometry", "color", "todonotes", "colortbl",
            "memoir", "zref", "moreverb"
        ]))
        with tempfile.TemporaryDirectory() as tmpdir:
            cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                tex_file = os.path.join(tmpdir, "dummy.tex")
                with open(tex_file, "w") as f:
                    f.write(r"\documentclass{test}")
                sys.argv = ["program", tex_file]
                if len(sig.parameters) == 0:
                    with contextlib.redirect_stdout(io.StringIO()):
                        assert main_obj() is None
                else:
                    with contextlib.redirect_stdout(io.StringIO()):
                        assert main_obj([]) is None
            finally:
                os.chdir(cwd)

def test_latex2nix_example_usage():
    if hasattr(tex2nix, "latex2nix"):
        input_tex = r"""
        \documentclass{scrreprt}
        \usepackage{fancyhdr}
        \usepackage{longtable}
        \begin{document}
        LaTeX public sample!
        \end{document}
        """
        pkgs = tex2nix.latex2nix(input_tex)
        assert isinstance(pkgs, list)
        assert 'fancyhdr' in pkgs
        assert 'longtable' in pkgs
        assert 'geometry' not in pkgs

def test_latex2nix_handles_empty():
    if hasattr(tex2nix, "latex2nix"):
        pkgs = tex2nix.latex2nix("")
        assert pkgs == []

def test_latex2nix_no_duplicates():
    if hasattr(tex2nix, "latex2nix"):
        input_tex = r"""
        \usepackage{todonotes}
        \usepackage{todonotes}
        \usepackage{colortbl}
        """
        pkgs = tex2nix.latex2nix(input_tex)
        assert pkgs.count('todonotes') == 1
        assert pkgs.count('colortbl') == 1

def test_latex2nix_custom_package():
    if hasattr(tex2nix, "latex2nix"):
        input_tex = r"""
        \documentclass{standalone}
        \usepackage{publicpackage}
        \begin{document}
        Public
        \end{document}
        """
        pkgs = tex2nix.latex2nix(input_tex)
        assert 'publicpackage' in pkgs

def test_latex2nix_multiline_usepackage():
    if hasattr(tex2nix, "latex2nix"):
        input_tex = r"""
        \usepackage{pgfplots,
        subcaption,
        caption}
        """
        pkgs = tex2nix.latex2nix(input_tex)
        for p in ['pgfplots','subcaption','caption']:
            assert p in pkgs

def test_latex2nix_with_comment_lines():
    if hasattr(tex2nix, "latex2nix"):
        input_tex = r"""
        % Just a comment line
        \usepackage{blindtext}
        % trailing comment
        """
        pkgs = tex2nix.latex2nix(input_tex)
        assert 'blindtext' in pkgs

def test_latex2nix_optional_arg():
    if hasattr(tex2nix, "latex2nix"):
        input_tex = r"""
        \usepackage[top=2cm]{geometry}
        \usepackage[usenames]{color}
        """
        pkgs = tex2nix.latex2nix(input_tex)
        assert 'geometry' in pkgs
        assert 'color' in pkgs

def test_latex2nix_ignores_unrelated_lines():
    if hasattr(tex2nix, "latex2nix"):
        input_tex = r"""
        123 random text line
        \date{}
        """
        pkgs = tex2nix.latex2nix(input_tex)
        assert pkgs == []

def test_detect_documentclass():
    if hasattr(tex2nix, "detect_documentclass"):
        input_tex = r"""
        \documentclass{memoir}
        \usepackage{zref}
        """
        docclass = tex2nix.detect_documentclass(input_tex)
        assert docclass == "memoir"

def test_detect_documentclass_none():
    if hasattr(tex2nix, "detect_documentclass"):
        input_tex = r"""
        % no docclass here
        \usepackage{moreverb}
        """
        docclass = tex2nix.detect_documentclass(input_tex)
        assert docclass is None