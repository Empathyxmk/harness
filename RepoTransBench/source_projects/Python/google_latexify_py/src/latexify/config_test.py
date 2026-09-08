from latexify import config

def test_merge_field_precedence_and_types():
    conf = config.Config.defaults().merge(
        expand_functions={"f"}, identifiers={"a": "b"}, prefixes={"p."}, reduce_assignments=True,
        use_math_symbols=True, use_set_symbols=True, use_signature=False, escape_underscores=False
    )
    merged = conf.merge(expand_functions=None)
    # The merged config should retain old expand_functions if new is None.
    assert merged.expand_functions == {"f"}  # changed from 'is None' to correct logic

def test_str_and_repr():
    conf = config.Config.defaults()
    s = str(conf)
    r = repr(conf)
    assert "expand_functions" in s and "expand_functions" in r

def test_defaults_is_a_config():
    c = config.Config.defaults()
    assert isinstance(c, config.Config)

def test_merge_different_types():
    c1 = config.Config.defaults()
    c2 = c1.merge(use_math_symbols=False)
    assert c2.use_math_symbols is False