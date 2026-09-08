def test_util_has_expected_methods():
    class Util:
        def getJobs(self): pass
        def getPathRelativeToTarget(self): pass
    util = Util()
    assert hasattr(util, 'getJobs')
    assert hasattr(util, 'getPathRelativeToTarget')