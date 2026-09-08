#!/usr/bin/env python3
"""
Public tests for OneFileLLM utility functions, different test data from private suite.
"""

import unittest
import os
import sys
import tempfile
import shutil
from utils import (
    safe_file_read,
    read_from_clipboard,
    read_from_stdin,
    detect_text_format,
    parse_as_plaintext,
    parse_as_markdown,
    parse_as_json,
    parse_as_html,
    parse_as_yaml,
    download_file,
    is_same_domain,
    is_within_depth,
    is_excluded_file,
    is_allowed_filetype,
    escape_xml,
    get_file_extension,
    is_binary_file
)

class TestUtilityFunctionsPublic(unittest.TestCase):
    """Test utility functions from utils.py with different data."""

    def setUp(self):
        self.tmpd = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpd)

    def test_safe_file_read_public(self):
        # UTF-8 file with different text
        f_utf8 = os.path.join(self.tmpd, "abc.txt")
        with open(f_utf8, 'w', encoding='utf-8') as f:
            f.write("Public 测试")
        content = safe_file_read(f_utf8)
        self.assertEqual(content, "Public 测试")

        # latin-1 file with different text
        f_latin1 = os.path.join(self.tmpd, "latinpublic.txt")
        with open(f_latin1, 'wb') as f:
            f.write("mañana".encode('latin-1'))
        self.assertEqual(safe_file_read(f_latin1), "mañana")

    def test_file_extension_detection_public(self):
        self.assertEqual(get_file_extension("some.JS"), ".js")
        self.assertEqual(get_file_extension("archive.TAR.GZ"), ".gz")
        self.assertEqual(get_file_extension("README"), "")
        self.assertEqual(get_file_extension("dots.with.many.parts.doc"), ".doc")

    def test_is_binary_file_public(self):
        # Text file
        t_file = os.path.join(self.tmpd, "t.txt")
        with open(t_file, 'w') as f:
            f.write("Sample text")
        self.assertFalse(is_binary_file(t_file))
        # Binary file
        b_file = os.path.join(self.tmpd, "b.dat")
        with open(b_file, 'wb') as f:
            f.write(b'\xff\xd8\xff\xdb')
        self.assertTrue(is_binary_file(b_file))

    def test_is_excluded_file_public(self):
        self.assertTrue(is_excluded_file("dist/bundle.js"))
        self.assertTrue(is_excluded_file(".git/hooks/pre-commit"))
        self.assertTrue(is_excluded_file("lib.min.js"))
        self.assertTrue(is_excluded_file("__pycache__/something.pyc"))
        self.assertTrue(is_excluded_file("node_modules/module.js"))
        self.assertFalse(is_excluded_file("main.c"))
        self.assertFalse(is_excluded_file("script.rb"))

    def test_is_allowed_filetype_public(self):
        self.assertTrue(is_allowed_filetype("index.html"))
        self.assertTrue(is_allowed_filetype("data.csv"))
        self.assertTrue(is_allowed_filetype("setup.py"))
        self.assertFalse(is_allowed_filetype("archive.tar.gz"))
        self.assertFalse(is_allowed_filetype("some.dll"))
        self.assertFalse(is_allowed_filetype("compressed.rar"))

    def test_url_utilities_public(self):
        base = "https://public.com/section/"
        self.assertTrue(is_same_domain(base, "https://public.com/else/"))
        self.assertFalse(is_same_domain(base, "https://alt.com/test/"))
        self.assertTrue(is_within_depth(base, "https://public.com/section/page2", 1))
        self.assertTrue(is_within_depth(base, "https://public.com/section/inner/page", 2))
        self.assertFalse(is_within_depth(base, "https://public.com/section/a/b/d", 2))

    def test_escape_xml_public(self):
        x = "<publicTest>More & stuff</publicTest>"
        self.assertEqual(escape_xml(x), x)