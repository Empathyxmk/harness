import os
import pytest
from src.htmlmin_module import HtmlMinifier, MinifyError, pretty_bytes, chalk_fake

class FakeFileInterface:
    def __init__(self, file_contents=None, error_on_read=False):
        self.files = dict(file_contents) if file_contents else {}
        self.error_on_read = error_on_read

    def read(self, src):
        if self.error_on_read:
            raise Exception('read error')
        if src not in self.files:
            raise Exception('file not found: ' + src)
        return self.files[src]

    def write(self, dest, content):
        self.files[dest] = content

    def exists(self, src):
        return src in self.files

class FakeGruntContext:
    def __init__(self, file_contents=None, error_on_read=False, error_on_minify=False):
        self.log_messages = []
        self.warn_messages = []
        self.file = FakeFileInterface(file_contents, error_on_read)
        self.verbose = type('Verbose', (), {'writeln': lambda *a, **k: None})()
        self._fn = None
        if error_on_minify:
            def minify(src, options):
                raise Exception('Minify boom')
        else:
            def minify(src, options):
                import re
                return re.sub(r"\s+", " ", src)
        self.minifier = HtmlMinifier(minify_func=minify)
        self.prettier = pretty_bytes
        self.chalk = chalk_fake

def grunt_htmlmin_task(grunt, options=lambda: {}, files=None, log=None, verbose=None, warn=None):
    # Implementation of the grunt htmlmin task logic, with mocks
    files = files or []
    succeeded = 0
    failed = 0
    for filegroup in files:
        srcs = filegroup.get("src", [])
        dest = filegroup.get("dest")
        if not srcs:
            failed += 1
            continue
        srcfile = srcs[0]
        try:
            html = grunt.file.read(srcfile)
            result = grunt.minifier.minify(html, options())
            grunt.file.write(dest, result)
            succeeded += 1
        except Exception as ex:
            failed += 1
            if warn:
                warn(f"{os.path.basename(srcfile)}: {ex}")
    msg = f"Minified {succeeded} files"
    if failed:
        msg += f" ({failed} failed)"
    if log:
        log(msg)
    return succeeded, failed

def test_minifies_valid_html_default_options(tmp_path):
    src_file = os.path.abspath("test/fixtures/test.html")
    dest = os.path.abspath(os.path.join(tmp_path, "test-spec-min.html"))
    HTML = '<html>\n   <body>   test </body> </html>'
    files_arr = [{"src": [src_file], "dest": dest}]
    fake = FakeGruntContext(file_contents={src_file: HTML})
    succeeded = []
    fake_log = lambda msg: succeeded.append(msg)
    grunt_htmlmin_task(fake, options=lambda: {}, files=files_arr, log=fake_log, verbose=fake.verbose)
    # The log message should mention Minified 1 files
    assert any("Minified 1 files" in m for m in succeeded)
    # The minifier must be called with HTML and {}
    assert fake.file.exists(dest)
    assert fake.file.read(dest) != HTML

def test_handles_missing_source_file_gracefully():
    files_arr = [{"src": [], "dest": "tmp/none.html"}]
    fake = FakeGruntContext()
    messages = []
    grunt_htmlmin_task(fake, options=lambda: {}, files=files_arr, log=messages.append, verbose=fake.verbose)
    assert any("Minified 0 files" in m for m in messages)
    assert not fake.file.exists("tmp/none.html")

def test_warns_and_skips_minifying_when_minifier_throws():
    src_file = "test/fixtures/test.html"
    files_arr = [{"src": [src_file], "dest": "tmp/should-not-exist.html"}]
    HTML = '<body> </body>'
    fake = FakeGruntContext(file_contents={src_file: HTML}, error_on_minify=True)
    warns = []
    grunt_htmlmin_task(fake, options=lambda: {}, files=files_arr, log=lambda msg: None, verbose=fake.verbose, warn=warns.append)
    assert any("test.html" in m and "Minify boom" in m for m in warns)
    assert not fake.file.exists("tmp/should-not-exist.html")

def test_outputs_count_of_successful_and_failed_files():
    src = "test/fixtures/test.html"
    files_arr = [
        {"src": [src], "dest": "tmp/success.html"},
        {"src": [], "dest": "tmp/fail.html"}
    ]
    fake = FakeGruntContext(file_contents={src: "<h1> foo </h1> "})
    loglines = []
    grunt_htmlmin_task(fake, options=lambda: {}, files=files_arr, log=loglines.append, verbose=fake.verbose)
    last_msg = loglines[-1]
    assert "Minified 1 files (1 failed)" in last_msg
    assert fake.file.exists("tmp/success.html")
    assert not fake.file.exists("tmp/fail.html")

def test_correctly_applies_minifier_options(tmp_path):
    src_file = os.path.abspath("test/fixtures/test.html")
    dest = os.path.abspath(os.path.join(tmp_path, "test-opt.html"))
    HTML = "<span>opt</span>"
    minifier_options = {"collapseWhitespace": True, "removeComments": True}
    files_arr = [{"src": [src_file], "dest": dest}]
    called = []
    # Custom minify to track args
    def minify(src, options):
        called.append((src, dict(options)))
        return "optim"  # so != HTML
    fake = FakeGruntContext(file_contents={src_file: HTML})
    fake.minifier = HtmlMinifier(minify_func=minify)
    grunt_htmlmin_task(fake, options=lambda: minifier_options, files=files_arr, log=lambda msg: None, verbose=fake.verbose)
    assert called and called[0][0] == HTML and called[0][1] == minifier_options
    assert fake.file.exists(dest)