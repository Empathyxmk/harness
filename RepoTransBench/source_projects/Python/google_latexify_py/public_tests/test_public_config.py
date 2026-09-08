"""Public tests for latexify.config.Config."""

from src.latexify import config


def test_merge_and_defaults_public():
    c = config.Config.defaults()

    # Change a value only, leave rest as default
    merged = c.merge(reduce_assignments=True)
    assert merged.reduce_assignments is True
    assert merged.use_math_symbols is False
    assert merged.expand_functions is None

    # Merge with another config
    c2 = config.Config.defaults().merge(use_set_symbols=True, use_signature=False)
    merged2 = c.merge(config=c2, use_signature=True)
    assert merged2.use_set_symbols is True
    assert merged2.use_signature is True
    assert merged2.escape_underscores is True

    # Test mutating mapping types
    merged3 = c.merge(identifiers={"z": "omega"})
    assert merged3.identifiers == {"z": "omega"}
    assert merged3.expand_functions is None

    # Test merging from config and kwargs precedence
    conf_a = c.merge(prefixes={"prefix"}).merge(use_signature=False)
    conf_b = config.Config.defaults().merge(use_set_symbols=True)
    result = conf_a.merge(config=conf_b)
    assert result.use_signature is True  # defaults from conf_b
    assert result.use_set_symbols is True

def test_config_defaults_public():
    defaults = config.Config.defaults()
    assert defaults.expand_functions is None
    assert defaults.identifiers is None
    assert defaults.prefixes is None
    assert defaults.reduce_assignments is False
    assert defaults.use_math_symbols is False
    assert defaults.use_set_symbols is False
    assert defaults.use_signature is True
    assert defaults.escape_underscores is True