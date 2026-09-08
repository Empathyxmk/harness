import pytest
from src.zapv2 import automation as automation_module

class DummyZAP:
    def __init__(self):
        self.base = 'BASE/'
        self.called = []
    def _request(self, url, params=None):
        self.called.append((url, params))
        return {'value': 'dummy'}

@pytest.fixture
def automation():
    return automation_module.automation(DummyZAP())

def test_plan_progress(automation):
    v = automation.plan_progress('myplan')
    assert v == {'value': 'dummy'}

def test_run_plan(automation):
    v = automation.run_plan('/tmp/file.yaml')
    assert v == 'dummy'

def test_end_delay_job(automation):
    v = automation.end_delay_job()
    assert v == 'dummy'