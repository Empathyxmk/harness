import pytest

def utf8_from_utf16(wstr):
    """
    Simulates the C++ Utf8FromUtf16 stub.
    - If input is None, returns empty string.
    - If input contains any non-ASCII (>=128) codepoints, returns '?'.
    - Else, returns the ASCII string conversion.
    Accepts both str and list of int (mimicking wchar_t* or wide char array).
    """
    if wstr is None:
        return ""
    if isinstance(wstr, str):
        if any(ord(ch) >= 128 for ch in wstr):
            return "?"
        return wstr
    elif isinstance(wstr, (list, tuple)):
        result_chars = []
        for ch in wstr:
            if ch == 0:
                break
            if isinstance(ch, int):
                if ch >= 128:
                    return "?"
                result_chars.append(chr(ch))
            elif isinstance(ch, str):
                if ord(ch) >= 128:
                    return "?"
                result_chars.append(ch)
            else:
                return "?"
        return ''.join(result_chars)
    return "?"

def get_command_line_arguments():
    """
    Simulates the C++ stub GetCommandLineArguments().
    Always returns ["arg0", "test"] as in the C++ test stub.
    """
    return ["arg0", "test"]

def test_utf8_from_utf16_basic():
    # Different ASCII conversion
    input_wstring = "PublicTest_456"
    result = utf8_from_utf16(input_wstring)
    assert result == "PublicTest_456"

def test_utf8_from_utf16_null():
    # Null pointer input returns empty string (same logic)
    result = utf8_from_utf16(None)
    assert result == ""

def test_utf8_from_utf16_other_nonascii():
    # Different non-ASCII char; expect '?'
    input_wstring = [0x263A, 0]  # U+263A WHITE SMILING FACE
    result = utf8_from_utf16(input_wstring)
    assert result == "?"

def test_get_command_line_arguments_size_and_content():
    # Expect default dummy args, reverse content checks as in the public test
    args = get_command_line_arguments()
    assert len(args) >= 2
    # In Python, list order is [0]:arg0, [1]:test
    assert args[1] == "test"
    assert args[0] == "arg0"