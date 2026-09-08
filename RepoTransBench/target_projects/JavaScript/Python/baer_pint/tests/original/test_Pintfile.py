def test_pintfile_exports_jobs_array():
    class Pintfile:
        jobs = ['test1', 'test2']
    pf = Pintfile
    assert hasattr(pf, 'jobs')
    assert isinstance(pf.jobs, list)