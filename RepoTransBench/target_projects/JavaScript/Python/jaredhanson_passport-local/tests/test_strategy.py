import pytest

from passport_local.strategy import Strategy, LocalStrategyError

def test_should_be_named_local():
    strategy = Strategy(lambda username, password, done=None: None)
    assert strategy.name == 'local'

def test_should_throw_if_constructed_without_verify():
    with pytest.raises(LocalStrategyError) as excinfo:
        Strategy()
    assert "LocalStrategy requires a verify callback" in str(excinfo.value)