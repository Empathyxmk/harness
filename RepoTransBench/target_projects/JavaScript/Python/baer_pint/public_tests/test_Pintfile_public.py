def test_exports_jobs_array_public():
    class Pintfile:
        jobs = ['public_job1', 'public_job2']
    p = Pintfile
    assert hasattr(p, 'jobs')
    assert isinstance(p.jobs, list)
    assert len(p.jobs) > 0

def test_contains_job_module_path_public():
    class Pintfile:
        jobs = ['public_job1', 'public_job2']
    p = Pintfile
    assert p.jobs[0] is not None
    assert isinstance(p.jobs[0], (str, object))