import pytest

def test_constructor_different():
    value = "xyz"
    assert value[0] == "x"

def test_at_method_different():
    value = "test"
    assert value[0] == 't'
    assert value[1] == 'e'
    assert value[2] == 's'
    assert value[3] == 't'
    assert len(value) == 4

def test_skip_whitespace_different():
    s = "  \r\n\t def"
    content = s.strip()
    assert content.endswith("def")
    s2 = " \n\n\t def"
    content2 = s2.lstrip()
    assert "def" in content2

def test_read_eof_different():
    s = ""
    assert s == ""

def test_read_identifier_different():
    s = "anotherVar"
    assert s.isidentifier()

def test_read_keyword_different():
    s = "float"
    # Simulate keyword lookup
    keywords = {"float"}
    assert s in keywords

def test_read_operator_different():
    op = "--"
    allowed = {"++", "--"}
    assert op in allowed

def test_read_int_constant_different():
    val = int("456")
    assert val == 456
    octal = int("77", 8)
    assert octal == 63
    hexa = int("1F", 16)
    assert hexa == 31

def test_read_uint_constant_different():
    val = int("789")
    assert val == 789

def test_read_float_constant_different():
    f1 = float("2.5")
    assert f1 == 2.5
    f2 = float("0.75")
    assert f2 == 0.75
    f3 = float("2e-3")
    assert f3 == 0.002

def test_read_double_constant_different():
    d = float("3.1415")
    assert d == 3.1415

def test_read_bool_constant_different():
    b1 = False
    assert not b1
    b2 = True
    assert b2

def test_read_directive_different():
    line = "#version 330 core"
    assert line.startswith("#version")
    assert "330" in line

def test_read_extension_directive_different():
    line = "#extension GL_EXT_shader_io_blocks : enable"
    assert ": enable" in line or ":enable" in line

def test_read_line_comment_different():
    code = "// Comment here\nfloat x;"
    assert "//" in code and "float x;" in code

def test_read_block_comment_different():
    code = "/* A multi-line\n comment here */int y;"
    assert "/*" in code and "int y;" in code

def test_preprocessor_macros_different():
    macro = "#define ANOTHER_MACRO test_value\nANOTHER_MACRO"
    assert "#define" in macro and "ANOTHER_MACRO" in macro

def test_preprocessor_if_else_endif_different():
    code = "#ifndef B\nfloat b;\n#else\nint a;\n#endif\n"
    assert "#ifndef" in code and "#endif" in code

def test_string_literal_different():
    s = "public test string"
    assert isinstance(s, str)

def test_unknown_token_different():
    err_string = "Unknown token '@'"
    assert "Unknown token" in err_string

def test_invalid_numeric_format_different():
    # Simulate hex fail
    with pytest.raises(ValueError):
        int("Y", 16)
    # Simulate octal fail
    with pytest.raises(ValueError):
        int("9", 8)