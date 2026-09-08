import pytest
from bumpversion.version_part import (
    VersionPart, NumericVersionPartConfiguration,
    ConfiguredVersionPartConfiguration, PartConfiguration
)

def test_version_part_default():
    vp = VersionPart('1')
    assert vp.value == '1'
    assert not vp.is_optional()
    assert vp.copy() == vp
    assert isinstance(format(vp, ''), str)
    assert isinstance(repr(vp), str)
    vp_bumped = vp.bump()
    assert vp_bumped.value == '2'

def test_version_part_with_configured():
    cfg = ConfiguredVersionPartConfiguration(['a', 'b'])
    vp = VersionPart('a', config=cfg)
    assert vp.value == 'a'
    vp2 = vp.bump()
    assert vp2.value == 'b'

def test_version_part_null_and_eq():
    cfg = NumericVersionPartConfiguration()
    vp = VersionPart('4', config=cfg)
    null_vp = vp.null()
    assert null_vp.value == cfg.first_value
    assert vp != null_vp
    vp2 = VersionPart('4', config=cfg)
    assert vp == vp2

def test_part_config_properties():
    cfg = NumericVersionPartConfiguration()
    assert cfg.first_value == '0'
    assert cfg.optional_value == '0'
    assert cfg.bump('9') == '10'