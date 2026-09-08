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
    # Accept str or list/tuple of ints/chars
    if isinstance(wstr, str):
        if any(ord(ch) >= 128 for ch in wstr):
            return "?"
        else:
            return wstr
    # e.g. for [0x20AC, 0] (list of ints, null-terminated)
    elif isinstance(wstr, (list, tuple)):
        result_chars = []
        for ch in wstr:
            if ch == 0:
                break
            if isinstance(ch, int):
                # handle euro sign, etc.
                if ch >= 128:
                    return "?"
                result_chars.append(chr(ch))
            elif isinstance(ch, str):
                if ord(ch) >= 128:
                    return "?"
                result_chars.append(ch)
            else:
                # unknown type
                return "?"
        return ''.join(result_chars)
    else:
        return "?"

def get_command_line_arguments():
    """
    Simulates the C++ stub GetCommandLineArguments().
    Always returns ["arg0", "test"], as in the C++ test stub.
    """
    return ["arg0", "test"]

def test_utf8_from_utf16_basic():
    # Basic conversion (ASCII-only, since non-ASCII won't be converted properly)
    input_wstring = "hello123!"
    result = utf8_from_utf16(input_wstring)
    assert result == "hello123!"

def test_utf8_from_utf16_null():
    # Null pointer input should return empty string
    result = utf8_from_utf16(None)
    assert result == ""

def test_utf8_from_utf16_nonascii():
    # Non-ASCII character should convert to "?"
    input_wstring = [0x20AC, 0]  # Euro sign (U+20AC)
    result = utf8_from_utf16(input_wstring)
    assert result == "?"

def test_get_command_line_arguments_not_empty():
    # Returns at least default dummy args
    args = get_command_line_arguments()
    assert len(args) >= 2
    assert args[0] == "arg0"
    assert args[1] == "test"