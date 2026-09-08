import pytest
from honcho.export import upstart

def test_get_job_name_public():
    assert upstart.get_job_name("myapp", "task", 4) == "myapp-task-4"
    assert upstart.get_job_name("zebra", "stripe", 7) == "zebra-stripe-7"

def test_get_master_name_public():
    assert upstart.get_master_name("newapp") == "newapp-master"
    assert upstart.get_master_name("rocket") == "rocket-master"