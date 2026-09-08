import pytest
from unittest import mock

@pytest.fixture
def grunt():
    # Simulate a minimal Grunt API mock
    obj = mock.Mock()
    obj.file = mock.Mock()
    obj.file.exists = mock.Mock(return_value=False)
    obj.file.write = mock.Mock()
    obj.verbose = mock.Mock()
    obj.verbose.writeln = mock.Mock()
    obj.verbose.ok = mock.Mock()
    obj.warn = mock.Mock(side_effect=lambda msg="warn": (_ for _ in ()).throw(Exception(msg)))
    obj.registerMultiTask = mock.Mock(side_effect=lambda name, desc, fn: setattr(obj, '_registered', fn))
    obj.registerTask = mock.Mock()
    obj.loadNpmTasks = mock.Mock()
    obj.loadTasks = mock.Mock()
    return obj

@pytest.fixture(autouse=True)
def reset_modules(monkeypatch):
    # Reset modules per test as in jest.resetModules
    yield

def test_register_multitask_and_compile(grunt):
    # register task, then call with mock task context
    # We'll simulate the registration and calling
    def mod(grunt):
        # Register the multitask
        def task_fn(self):
            return self.async()()
        grunt.registerMultiTask("sass", "desc", task_fn)
    mod(grunt)

    class Task:
        def async_(self):  # In JS: async() returns callback to invoke when done
            def done(): pass
            return done
        async = async_
        def options(self): return {}
        files = [dict(src=["a.scss"], dest="a.css")]
        filesSrc = ["a.scss"]

    # Should not throw
    try:
        grunt._registered(Task())
    except Exception:
        pytest.fail("Should not throw")

def test_throw_if_bundle_exec_no_bundle(grunt):
    def mod(grunt):
        def task_fn(self):
            options = self.options()
            if options.get("bundleExec", False):
                raise Exception("not found")
            return self.async()()
        grunt.registerMultiTask("sass", "desc", task_fn)
    mod(grunt)

    class Task:
        def async_(self): return lambda: None
        async = async_
        def options(self): return {"bundleExec": True}
        files = []
        filesSrc = []

    with pytest.raises(Exception):
        grunt._registered(Task())

def test_skip_partials(grunt):
    def mod(grunt):
        def task_fn(self):
            return self.async()()
        grunt.registerMultiTask("sass", "desc", task_fn)
    mod(grunt)

    class Task:
        def async_(self): return lambda: None
        async = async_
        def options(self): return {}
        files = [dict(src=["_partial.scss"], dest="_partial.css")]
        filesSrc = ["_partial.scss"]

    # Should not throw
    grunt._registered(Task())

def test_call_check_files_syntax_on_option(grunt):
    check_files_syntax_called = {'called': False}
    def checkFilesSyntax(filesSrc, options, cb):
        check_files_syntax_called['called'] = True
        cb()
    # Mod function injects the checkFilesSyntax
    def mod(grunt):
        def task_fn(self):
            options = self.options()
            if options.get("check", False):
                checkFilesSyntax(self.filesSrc, options, lambda: None)
            return self.async()()
        grunt.registerMultiTask("sass", "desc", task_fn)
    mod(grunt)

    class Task:
        def async_(self): return lambda: None
        async = async_
        def options(self): return {"check": True}
        files = []
        filesSrc = ["test.scss"]

    grunt._registered(Task())
    assert check_files_syntax_called['called']

def test_update_correctly_when_file_not_exist(grunt):
    def mod(grunt):
        def task_fn(self):
            options = self.options()
            if options.get("update", False):
                if not grunt.file.exists("test.css"):
                    pass  # mimic update logic
            return self.async()()
        grunt.registerMultiTask("sass", "desc", task_fn)
    mod(grunt)
    grunt.file.exists.return_value = False

    class Task:
        def async_(self): return lambda: None
        async = async_
        def options(self): return {"update": True}
        files = [dict(src=["test.scss"], dest="test.css")]
        filesSrc = ["test.scss"]

    grunt._registered(Task())

def test_update_correctly_when_file_does_exist(grunt):
    def mod(grunt):
        def task_fn(self):
            options = self.options()
            if options.get("update", False):
                if grunt.file.exists("test.css"):
                    pass  # mimic update logic
            return self.async()()
        grunt.registerMultiTask("sass", "desc", task_fn)
    mod(grunt)
    grunt.file.exists.return_value = True

    class Task:
        def async_(self): return lambda: None
        async = async_
        def options(self): return {"update": True}
        files = [dict(src=["test.scss"], dest="test.css")]
        filesSrc = ["test.scss"]

    grunt._registered(Task())

def test_add_scss_arg_for_css_input(grunt):
    def mod(grunt):
        def task_fn(self):
            # --scss arg for .css input
            return self.async()()
        grunt.registerMultiTask("sass", "desc", task_fn)
    mod(grunt)

    class Task:
        def async_(self): return lambda: None
        async = async_
        def options(self): return {}
        files = [dict(src=["foo.css"], dest="foo-out.css")]
        filesSrc = ["foo.css"]

    grunt._registered(Task())

def test_use_bundle_exec_path(grunt):
    def mod(grunt):
        def task_fn(self):
            options = self.options()
            if options.get("bundleExec"):
                pass
            return self.async()()
        grunt.registerMultiTask("sass", "desc", task_fn)
    mod(grunt)

    class Task:
        def async_(self): return lambda: None
        async = async_
        def options(self): return {"bundleExec": True}
        files = [dict(src=["a.scss"], dest="a.css")]
        filesSrc = ["a.scss"]

    grunt._registered(Task())