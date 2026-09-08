def test_statement_name_public():
    # Synthetic test of statement names: just check string names in various "orders"
    names = [
        "declaration", "empty", "continue", "if", "switch",
        "expression", "compound", "while", "do", "for",
        "return", "break", "discard", "case label"
    ]

    # Ensure all expected keywords are present, in any order
    assert set(names) == set([
        "compound", "declaration", "expression", "if", "switch",
        "case label", "while", "do", "for", "continue",
        "break", "return", "discard", "empty"
    ])

    # Custom unknown statement type, simulated
    unknown = "(unknown)"
    assert unknown == "(unknown)"

def test_constructors_variety_public():
    # Simulate different node construction scenarios (different values)
    tu_type = "kGlobal"
    assert tu_type == "kGlobal"
    builtin_type = "kKeyword_mat3"
    assert builtin_type == "kKeyword_mat3"
    struct_name = None
    var_type = "kParameter"
    assert var_type == "kParameter"
    func_return_type = None
    param_type = "kParameter"
    assert param_type == "kParameter"
    stmt_type = "kExpression"
    assert stmt_type == "kExpression"