import sys
import os
import importlib

# Ensure tex2nix can be imported when running from public_tests directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tex2nix")))

tex2nix = importlib.import_module("__init__")

def test_full_tex2nix_pipeline():
    if hasattr(tex2nix, "latex2nix") and hasattr(tex2nix, "detect_documentclass"):
        tex_example = r"""
        \documentclass[10pt]{report}
        \usepackage{pdfpages}
        \usepackage{mhchem}
        """
        pkgs = tex2nix.latex2nix(tex_example)
        assert 'pdfpages' in pkgs
        assert 'mhchem' in pkgs
        assert pkgs.count('pdfpages') == 1
        docclass = tex2nix.detect_documentclass(tex_example)
        assert docclass == "report"