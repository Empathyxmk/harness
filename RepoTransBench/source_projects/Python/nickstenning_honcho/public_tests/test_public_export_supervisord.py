import pytest
from honcho.export import supervisord

def test_get_program_name_public():
    assert supervisord.get_program_name("supapp", "qwe", 9) == "supapp-qwe-9"
    assert supervisord.get_program_name("jazz", "band", 4) == "jazz-band-4"

def test_get_master_name_public():
    assert supervisord.get_master_name("testfoo") == "testfoo-master"
    assert supervisord.get_master_name("lemur") == "lemur-master"