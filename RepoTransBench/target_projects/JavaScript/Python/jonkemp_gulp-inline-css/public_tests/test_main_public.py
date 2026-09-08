import os
import io
import sys
import types
import pytest

# Assuming the 'inline_css' implementation is provided in 'src/inline_css.py' as 'inline_css' callable.
# This will be a placeholder for the pipeline pattern used in gulp plugins.
# In an actual translation, you should provide a drop-in replacement for 'inlineCss' with compatible API.

from src.inline_css import inline_css

class FakeFile:
    """
    Emulates a simple file object similar to Vinyl in gulp.
    """
    def __init__(self, path, contents=None):
        self.path = os.path.abspath(path)
        self.contents = contents  # Should be bytes or None

    def is_buffer(self):
        return isinstance(self.contents, (bytes, bytearray))

    @property
    def relative(self):
        return os.path.basename(self.path)


# Utilities mirroring JavaScript helper functions

def get_file(file_path):
    with open(file_path, "rb") as f:
        content = f.read()
    return FakeFile(file_path, content)


def compare(fixture_path, expected_path, options, done):
    """
    Compare the output of inlining with an expected result.
    'options' may be used for configuration if supported by the inline_css function.
    'done' is a callback invoked upon completion.
    """
    stream = inline_css(options)
    # Write the file to the stream (simulate as a push)
    file_obj = get_file(fixture_path)
    out_list = []

    def on_data(out_file):
        assert out_file.is_buffer()
        with open(expected_path, "rb") as f:
            expected_content = f.read()
        assert out_file.contents == expected_content
        done()

    # Simulate streaming and callback pattern
    stream.write(file_obj, on_data)


def fake_callback():
    # Used as a placeholder for a no-op callback
    pass


def test_file_should_pass_through_using_different_content(tmp_path):
    """
    file should pass through using different content
    """
    class EndSignal(Exception): pass

    a = [0]
    fake_file_path = tmp_path / "testfile.html"
    contents = b"Public Test Case!"
    fake_file_path.write_bytes(contents)

    fake_file = FakeFile(str(fake_file_path), contents)

    # inline_css returns a "stream" object with write() and end() methods.
    stream = inline_css()  # No options

    writes = []
    ended = []

    def on_data(new_file):
        assert new_file.contents is not None
        assert new_file.path == str(fake_file_path)
        assert new_file.relative == "testfile.html"
        a[0] += 1

    def on_end():
        assert a[0] == 1
        raise EndSignal()

    stream.on_data = on_data
    stream.on_end = on_end

    try:
        stream.write(fake_file)
        stream.end()
    except EndSignal:
        pass

def test_should_let_null_files_pass_through(tmp_path):
    """
    should let null files pass through (public)
    """
    class EndSignal(Exception): pass

    n = [0]

    stream = inline_css()  # No options

    def pipe(file):
        assert file.path == "public-null.md"
        assert file.contents is None
        n[0] += 1

    def on_end():
        assert n[0] == 1
        raise EndSignal()

    stream.pipe = pipe
    stream.on_end = on_end

    null_file = FakeFile("public-null.md", None)

    try:
        stream.write(null_file)
        stream.end()
    except EndSignal:
        pass

def test_should_emit_error_on_streamed_file(tmp_path):
    """
    should emit error on streamed file (public)
    """
    class ErrorSignal(Exception):
        def __init__(self, message):
            super().__init__(message)
            self.message = message

    fixture_path = os.path.join("public_tests", "fixtures", "inline.html")
    # If the implementation uses a 'buffer' option, pass it as {buffer=False}. Otherwise, simulate streamed input.
    streamed = inline_css()

    def on_error(err):
        assert getattr(err, "message", "") == "Streaming not supported"
        raise ErrorSignal("Streaming not supported")

    streamed.on_error = on_error

    # Simulate writing a streamed file
    class StreamedFile(FakeFile):
        # Mark as a 'stream', not buffer
        def is_buffer(self):
            return False

    file_obj = StreamedFile(fixture_path, contents=None)
    file_obj.streamed = True  # custom field if needed

    with pytest.raises(ErrorSignal) as excinfo:
        streamed.write(file_obj)
    assert "Streaming not supported" in str(excinfo.value)

def test_should_convert_linked_css_to_inline_css(tmp_path):
    """
    Should convert linked css to inline css (public/alt data)
    """
    done = [False]

    def mark_done():
        done[0] = True

    options = {}
    fixture_path = os.path.join("public_tests", "fixtures", "inline.html")
    expected_path = os.path.join("public_tests", "expected", "inline-expected.html")
    compare(fixture_path, expected_path, options, mark_done)
    assert done[0]

def test_should_inline_css_in_multiple_html_files(tmp_path):
    """
    Should inline css in multiple HTML files (public/alt data)
    """
    done = [False]
    options = {}

    def mark_done():
        done[0] = True

    fixture_path_1 = os.path.join("public_tests", "fixtures", "group", "alpha", "inline.html")
    expected_path_1 = os.path.join("public_tests", "expected", "group", "alpha", "inline-expected.html")

    # first: just test run, no assertion
    compare(fixture_path_1, expected_path_1, options, lambda: None)

    fixture_path_2 = os.path.join("public_tests", "fixtures", "group", "beta", "inline.html")
    expected_path_2 = os.path.join("public_tests", "expected", "group", "beta", "inline-expected.html")
    compare(fixture_path_2, expected_path_2, options, mark_done)
    assert done[0]

def test_should_ignore_hbs_code_blocks(tmp_path):
    """
    Should ignore hbs code blocks (public)
    """
    done = [False]
    def mark_done():
        done[0] = True
    options = {}
    fixture_path = os.path.join("public_tests", "fixtures", "codeblocks-public.html")
    expected_path = os.path.join("public_tests", "expected", "codeblocks-public.html")
    compare(fixture_path, expected_path, options, mark_done)
    assert done[0]

def test_should_ignore_user_defined_code_blocks(tmp_path):
    """
    Should ignore user defined code blocks (public)
    """
    done = [False]
    def mark_done():
        done[0] = True
    options = {'codeBlocks': {'special': {'start': '<!', 'end': '!>'}}}
    fixture_path = os.path.join("public_tests", "fixtures", "codeblocks-external-public.html")
    expected_path = os.path.join("public_tests", "expected", "codeblocks-external-public.html")
    compare(fixture_path, expected_path, options, mark_done)
    assert done[0]