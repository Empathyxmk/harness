import pytest
import cloudconvert.job as job

def test_job_from_data():
    # Partial coverage, check construction
    data = {'id': 'abc', 'status': 'waiting'}
    j = job.Job(data)
    assert j['id'] == 'abc'
    assert j['status'] == 'waiting'

def test_job_str_repr():
    d = {'id': 'a', 'foo': 'b'}
    j = job.Job(d)
    assert 'id' in str(j)
    assert 'foo' in repr(j)

def test_job_fail_missing_key():
    # Should allow missing keys
    j = job.Job({})
    assert isinstance(j, job.Job)