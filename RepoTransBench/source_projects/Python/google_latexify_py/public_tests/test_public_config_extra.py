"""Extra public tests for latexify.config.Config with additional/different settings."""

from src.latexify import config


def test_merge_explicit_keys_public():
    c = config.Config.defaults()
    merged = c.merge(escape_underscores=False, use_signature=False)
    assert merged.escape_underscores is False
    assert merged.use_signature is False
    assert merged.reduce_assignments is c.reduce_assignments

    # Merge with sets for prefixes/expand_functions
    m2 = c.merge(prefixes={"foo.bar", "baz.invalid"}, expand_functions={"fn"})
    assert m2.prefixes == {"foo.bar", "baz.invalid"}
    assert m2.expand_functions == {"fn"}

    # Overriding by config param
    c_other = c.merge(use_math_symbols=True)
    m3 = c.merge(config=c_other)
    assert m3.use_math_symbols is True
    assert m3.reduce_assignments is c.reduce_assignments
    assert m3.escape_underscores is True