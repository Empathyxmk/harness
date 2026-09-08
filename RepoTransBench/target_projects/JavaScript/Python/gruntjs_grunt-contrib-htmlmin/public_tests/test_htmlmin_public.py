import os
import pytest
from src.htmlmin_module import HtmlMinifier, MinifyError, pretty_bytes_public, chalk_fake

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
                raise Exception('Public Minifier Broken')
        else:
            import re
            def minify(src, options):
                # Remove all spaces (replicating JS / +/g, '')
                return re.sub(r" +", "", src)
        self.minifier = HtmlMinifier(minify_func=minify)
        self.prettier = pretty_bytes_public
        self.chalk = chalk_fake

def grunt_htmlmin_task(grunt, options=lambda: {}, files=None, log=None, verbose=None, warn=None):
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

def test_minifies_another_valid_html_file_default_options_public(tmp_path):
    src_file = os.path.abspath("test/fixtures/public_input.html")
    dest = os.path.abspath(os.path.join(tmp_path, "public-test-spec-min.html"))
    HTML = "<div>   <p>hello public</p>\n</div>"
    files_arr = [{"src": [src_file], "dest": dest}]
    fake = FakeGruntContext(file_contents={src_file: HTML})
    messages = []
    grunt_htmlmin_task(fake, options=lambda: {}, files=files_arr, log=messages.append, verbose=fake.verbose)
    assert any("Minified 1 files" in m for m in messages)
    assert fake.file.exists(dest)
    # Should have been minified (spaces removed)
    assert fake.file.read(dest) != HTML

def test_handles_missing_public_source_file_gracefully():
    files_arr = [{"src": [], "dest": "tmp/public-none.html"}]
    fake = FakeGruntContext()
    messages = []
    grunt_htmlmin_task(fake, options=lambda: {}, files=files_arr, log=messages.append, verbose=fake.verbose)
    assert any("Minified 0 files" in m for m in messages)
    assert not fake.file.exists("tmp/public-none.html")

def test_warns_and_skips_minifying_when_minifier_throws_public():
    src_file = "test/fixtures/public_input.html"
    files_arr = [{"src": [src_file], "dest": "tmp/public-should-not-exist.html"}]
    HTML = "<header> error </header>"
    fake = FakeGruntContext(file_contents={src_file: HTML}, error_on_minify=True)
    warns = []
    grunt_htmlmin_task(fake, options=lambda: {}, files=files_arr, log=lambda msg: None, verbose=fake.verbose, warn=warns.append)
    assert any("public_input.html" in m and "Public Minifier Broken" in m for m in warns)
    assert not fake.file.exists("tmp/public-should-not-exist.html")

def test_outputs_count_of_successful_and_failed_files_public():
    src = "test/fixtures/public_input.html"
    files_arr = [
        {"src": [src], "dest": "tmp/public-success.html"},
        {"src": [], "dest": "tmp/public-fail.html"}
    ]
    fake = FakeGruntContext(file_contents={src: "<table> doctype </table>"})
    loglines = []
    grunt_htmlmin_task(fake, options=lambda: {}, files=files_arr, log=loglines.append, verbose=fake.verbose)
    last_msg = loglines[-1]
    assert "Minified 1 files (1 failed)" in last_msg
    assert fake.file.exists("tmp/public-success.html")
    assert not fake.file.exists("tmp/public-fail.html")

def test_correctly_applies_different_minifier_options_public(tmp_path):
    src_file = os.path.abspath("test/fixtures/public_input.html")
    dest = os.path.abspath(os.path.join(tmp_path, "public-test-opt.html"))
    HTML = "<section>section-test</section>"
    minifier_options = {"minifyJS": True, "decodeEntities": True}
    files_arr = [{"src": [src_file], "dest": dest}]
    called = []
    def minify(src, options):
        called.append((src, dict(options)))
        return "sectioned"
    fake = FakeGruntContext(file_contents={src_file: HTML})
    fake.minifier = HtmlMinifier(minify_func=minify)
    grunt_htmlmin_task(fake, options=lambda: minifier_options, files=files_arr, log=lambda msg: None, verbose=fake.verbose)
    assert called and called[0][0] == HTML and called[0][1] == minifier_options
    assert fake.file.exists(dest)