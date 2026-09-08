def test_util_has_getJobs_and_getOptions_functions():
    class Util:
        def getJobs(self, config):
            return ['jobA', 'jobB']
        def getOptions(self, options_dict):
            return {'foo': options_dict.get('foo'), 'baz': options_dict.get('baz')}
    util = Util()
    assert hasattr(util, 'getJobs')
    assert callable(util.getJobs)
    assert hasattr(util, 'getOptions')
    assert callable(util.getOptions)

def test_util_getJobs_returns_array_for_different_config():
    class Util:
        def getJobs(self, config):
            return ['jobA', 'jobB']
        def getOptions(self, options_dict):
            return {'foo': options_dict.get('foo'), 'baz': options_dict.get('baz')}
    util = Util()
    jobs = util.getJobs({'testKey': 'public-value'})
    assert isinstance(jobs, list)

def test_util_getOptions_processes_different_options_object():
    class Util:
        def getJobs(self, config):
            return ['jobA', 'jobB']
        def getOptions(self, options_dict):
            return {'foo': options_dict.get('foo'), 'baz': options_dict.get('baz')}
    util = Util()
    opts = util.getOptions({'foo': 'bar', 'baz': 123})
    assert isinstance(opts, dict)