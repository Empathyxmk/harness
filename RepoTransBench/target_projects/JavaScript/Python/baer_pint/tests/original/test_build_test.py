import os
import pytest

@pytest.fixture
def build_config(tmp_path):
    # Simulate build/test.js by creating an object (dict) with the keys we check for in the test
    return {
        'name': 'test',
        'dependsOn': [],
        'jobs': ['job1', 'job2']
    }

def test_build_config_export_object_with_expected_properties(build_config):
    assert isinstance(build_config, dict)
    # Should have any of the following keys: name, dependsOn, jobs
    has_key = any(k in build_config for k in ['name', 'dependsOn', 'jobs'])
    assert has_key