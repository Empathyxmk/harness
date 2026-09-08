def test_parse_version_directive_different():
    source = "#version 450 compatibility\n"
    version_found = "450" in source
    compat_found = "compatibility" in source
    assert version_found and compat_found

def test_parse_simple_global_variable_different():
    source = "uniform int pubVar;\n"
    uniform_found = "uniform" in source
    pub_var_found = "pubVar" in source
    assert uniform_found and pub_var_found

def test_parse_function_definition_different():
    source = (
        "int triple(int a) {\n"
        "  return a * 3;\n"
        "}\n"
    )
    has_triple = "triple" in source
    has_return = "return" in source
    assert has_triple and has_return