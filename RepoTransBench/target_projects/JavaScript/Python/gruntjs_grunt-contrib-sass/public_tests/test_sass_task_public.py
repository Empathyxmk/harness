import pytest
from unittest import mock

@pytest.fixture
def grunt():
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
    yield

def test_register_multitask_new_compile(grunt):
    def mod(grunt):
        def task_fn(self):
            return self.async()()
        grunt.registerMultiTask("sass", "desc", task_fn)
    mod(grunt)

    class Task:
        def async_(self): return lambda: None
        async = async_
        def options(self): return {}
        files = [dict(src=["b.scss"], dest="b.css")]
        filesSrc = ["b.scss"]
    try:
        grunt._registered(Task())
    except Exception:
        pytest.fail("Should not throw")

def test_throw_if_bundle_exec_no_bundle_public(grunt):
    def mod(grunt):
        def task_fn(self):
            options = self.options()
            if options.get("bundleExec", False):
                raise Exception("notfoundpublic")
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

def test_skip_new_partial_public(grunt):
    def mod(grunt):
        def task_fn(self):
            return self.async()()
        grunt.registerMultiTask("sass", "desc", task_fn)
    mod(grunt)
    class Task:
        def async_(self): return lambda: None
        async = async_
        def options(self): return {}
        files = [dict(src=["_widget.scss"], dest="_widget.css")]
        filesSrc = ["_widget.scss"]
    grunt._registered(Task())

def test_call_check_files_syntax_when_options_check_public(grunt):
    check_files_syntax_called = {'called': False}
    def checkFilesSyntax(filesSrc, options, cb):
        check_files_syntax_called['called'] = True
        cb()
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
        filesSrc = ["publictest.scss"]
    grunt._registered(Task())
    assert check_files_syntax_called['called']

def test_update_when_file_not_exist_public(grunt):
    def mod(grunt):
        def task_fn(self):
            options = self.options()
            if options.get("update", False):
                if not grunt.file.exists("public.css"):
                    pass
            return self.async()()
        grunt.registerMultiTask("sass", "desc", task_fn)
    mod(grunt)
    grunt.file.exists.return_value = False
    class Task:
        def async_(self): return lambda: None
        async = async_
        def options(self): return {"update": True}
        files = [dict(src=["public.scss"], dest="public.css")]
        filesSrc = ["public.scss"]
    grunt._registered(Task())

def test_update_when_file_exists_public(grunt):
    def mod(grunt):
        def task_fn(self):
            options = self.options()
            if options.get("update", False):
                if grunt.file.exists("public.css"):
                    pass
            return self.async()()
        grunt.registerMultiTask("sass", "desc", task_fn)
    mod(grunt)
    grunt.file.exists.return_value = True
    class Task:
        def async_(self): return lambda: None
        async = async_
        def options(self): return {"update": True}
        files = [dict(src=["public.scss"], dest="public.css")]
        filesSrc = ["public.scss"]
    grunt._registered(Task())

def test_add_scss_arg_for_publiccss_input(grunt):
    def mod(grunt):
        def task_fn(self):
            return self.async()()
        grunt.registerMultiTask("sass", "desc", task_fn)
    mod(grunt)
    class Task:
        def async_(self): return lambda: None
        async = async_
        def options(self): return {}
        files = [dict(src=["bar.css"], dest="bar-out.css")]
        filesSrc = ["bar.css"]
    grunt._registered(Task())

def test_use_bundle_exec_path_public(grunt):
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
        files = [dict(src=["c.scss"], dest="c.css")]
        filesSrc = ["c.scss"]
    grunt._registered(Task())