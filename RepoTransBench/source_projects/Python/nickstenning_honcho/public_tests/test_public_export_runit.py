import pytest
from honcho.export import runit

def test_get_service_name_public():
    assert runit.get_service_name("xyapp", "cache", 2) == "xyapp-cache-2"
    assert runit.get_service_name("dragon", "fire", 1) == "dragon-fire-1"

def test_get_log_service_name_public():
    assert runit.get_log_service_name("xyapp", "cache", 2) == "xyapp-cache-2-log"
    assert runit.get_log_service_name("lion", "roar", 3) == "lion-roar-3-log"