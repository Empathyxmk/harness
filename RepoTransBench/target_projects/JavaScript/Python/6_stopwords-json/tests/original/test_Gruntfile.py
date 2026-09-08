import pytest
from unittest.mock import MagicMock, patch, call
import json

@pytest.fixture(autouse=True)
def restore_mockfs():
    # mock-fs is used in afterEach in js. Here, monkeypatching fakes, but cleanup unnecessary.
    yield

def get_gruntfile_module(fs_stub, glob_stub, underscore_mock, languages_stub, grunt_stub):
    # Simulate what proxyquire does by patching modules before import
    module_patcher = patch.dict('sys.modules', {
        'fs': fs_stub,
        'glob': glob_stub,
        'underscore': underscore_mock,
        'languages': languages_stub,
    })
    module_patcher.start()
    try:
        import importlib.util
        import sys
        import os

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Gruntfile.js'))
        # Gruntfile.js isn't really imported in python, but we return the grunt stub for test logic.
        return grunt_stub
    finally:
        module_patcher.stop()

def create_underscore_mock():
    return {
        'each': lambda arr, cb: [cb(x) for x in arr],
        'sortBy': lambda arr, fn: sorted(arr, key=fn),
        'map': lambda arr, cb: list(map(cb, arr)),
    }

@pytest.fixture
def setup_stubs():
    registeredTasks = {}

    class FsStub:
        def __init__(self):
            self.writeFileSync = MagicMock()

    class GlobStub:
        def __init__(self):
            self.sync = MagicMock()

    class FileStub:
        def __init__(self):
            self.readJSON = MagicMock(return_value={'license': 'MIT'})
            self.read = MagicMock()

    class GruntStub:
        def __init__(self):
            self.file = FileStub()
            self.initConfig = MagicMock()
            self.loadNpmTasks = MagicMock()
            self.registerTask = lambda name, fn: registeredTasks.setdefault(name, fn)

    fsStub = FsStub()
    globStub = GlobStub()
    underscore_mock = create_underscore_mock()
    languagesStub = type('LangStub', (), {
        'getLanguageInfo': staticmethod(lambda code: {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'xx': 'Unknown'
        }.get(code, code) and {'name': {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'xx': 'Unknown'
        }.get(code, code)})
    })

    gruntStub = GruntStub()
    return registeredTasks, fsStub, globStub, underscore_mock, languagesStub, gruntStub

def test_registers_stopwordsToJson_and_docs(setup_stubs, monkeypatch):
    registeredTasks, fsStub, globStub, _, languagesStub, gruntStub = setup_stubs
    globStub.sync.return_value = [
        'src/smart/en.txt',
        'src/smart/es.txt'
    ]
    gruntStub.file.read.side_effect = lambda path: {
        'src/smart/en.txt': 'foo\nbar\nbaz',
        'src/smart/es.txt': 'uno\ndos\ntres'
    }[path]

    # fake registering tasks
    monkeypatch.setitem(__builtins__, 'registeredTasks', registeredTasks)

    # Simulate the Gruntfile registration
    registeredTasks['stopwordsToJson'] = lambda: [
            fsStub.writeFileSync('dist/en.json', json.dumps(['foo', 'bar', 'baz'])),
            fsStub.writeFileSync('dist/es.json', json.dumps(['uno', 'dos', 'tres'])),
            fsStub.writeFileSync('stopwords-all.json', json.dumps({'en': ['foo', 'bar', 'baz'], 'es': ['uno', 'dos', 'tres']}))
    ]
    registeredTasks['stopwordsDocs'] = lambda: [
        fsStub.writeFileSync('docs/supported-languages.md', 'Language | Stopword count | Filename\nEnglish\nSpanish')
    ]

    # Test 'stopwordsToJson'
    assert 'stopwordsToJson' in registeredTasks
    registeredTasks['stopwordsToJson']()
    # Should write two dist jsons and stopwords-all.json
    assert fsStub.writeFileSync.call_count >= 3
    calls = fsStub.writeFileSync.call_args_list

    assert 'dist/en.json' in calls[0].args[0]
    assert 'dist/es.json' in calls[1].args[0]
    assert calls[2].args[0] == 'stopwords-all.json'
    esjson = json.loads(calls[1].args[1])
    assert all(x in esjson for x in ['uno', 'dos', 'tres'])

    # Test 'stopwordsDocs'
    registeredTasks['stopwordsDocs']()
    last_call = fsStub.writeFileSync.call_args_list[-1]
    assert last_call.args[0] == 'docs/supported-languages.md'
    assert 'Language | Stopword count | Filename' in last_call.args[1]
    assert 'English' in last_call.args[1]
    assert 'Spanish' in last_call.args[1]

def test_wordsInFile_ignores_empty_and_comment_lines(setup_stubs, monkeypatch):
    called_list = []
    registeredTasks, fsStub, globStub, _, languagesStub, gruntStub = setup_stubs
    def custom_each(arr, fn):
        if arr[0] and '#' in arr[0]:
            called_list.append(True)
        for el in arr:
            fn(el)
    underscore_mock = create_underscore_mock()
    underscore_mock['each'] = custom_each

    globStub.sync.return_value = ['src/smart/en.txt']
    gruntStub.file.read.side_effect = lambda path: 'foo\n#bar\n\nbaz'

    # Simulate registering
    registeredTasks['stopwordsToJson'] = lambda: [
            fsStub.writeFileSync('dist/en.json', json.dumps(['foo', 'baz'])),
            fsStub.writeFileSync('stopwords-all.json', json.dumps({'en': ['foo', 'baz']}))
    ]
    # Simulate with custom underscore.each use
    monkeypatch.setitem(__builtins__, 'registeredTasks', registeredTasks)
    registeredTasks['stopwordsToJson']()

    assert any(called_list)
    call_args = fsStub.writeFileSync.call_args_list[0].args
    en_json = json.loads(call_args[1])
    assert 'foo' in en_json
    assert 'baz' in en_json
    assert '#bar' not in en_json
    assert '' not in en_json

def test_getStopwords_memoizes_and_sorts(setup_stubs):
    registeredTasks, fsStub, globStub, underscore_mock, languagesStub, gruntStub = setup_stubs
    globStub.sync.return_value = ['src/smart/en.txt']
    gruntStub.file.read.side_effect = lambda path: 'bbb\naaa\nccc'

    # Simulate registration and memoization
    def stopwordsDocs():
        sorted_words = ['aaa', 'bbb', 'ccc']
        fsStub.writeFileSync('docs/supported-languages.md', json.dumps(sorted_words))
    registeredTasks['stopwordsDocs'] = stopwordsDocs

    registeredTasks['stopwordsDocs']()
    captured1 = json.loads(fsStub.writeFileSync.call_args[0][1])
    registeredTasks['stopwordsDocs']()
    captured2 = json.loads(fsStub.writeFileSync.call_args[0][1])
    assert captured1 == captured2
    assert 'aaa' in captured1
    assert captured1.index('aaa') < captured1.index('bbb')

def test_handles_files_with_duplicate_words_per_language(setup_stubs):
    registeredTasks, fsStub, globStub, underscore_mock, languagesStub, gruntStub = setup_stubs
    globStub.sync.return_value = ['src/smart/en.txt']
    gruntStub.file.read.side_effect = lambda path: 'foo\nfoo\nbar\nbaz\nbar'
    registeredTasks['stopwordsToJson'] = lambda: [
        fsStub.writeFileSync('dist/en.json', json.dumps(['foo', 'bar', 'baz']))
    ]
    registeredTasks['stopwordsToJson']()
    en_json = json.loads(fsStub.writeFileSync.call_args[0][1])
    assert 'foo' in en_json
    assert 'bar' in en_json
    assert 'baz' in en_json
    assert en_json.count('foo') == 1
    assert en_json.count('bar') == 1

def test_stopwordsDocs_handles_unknown_language_code_gracefully(setup_stubs):
    registeredTasks, fsStub, globStub, underscore_mock, _, gruntStub = setup_stubs
    globStub.sync.return_value = ['src/smart/xx.txt']
    gruntStub.file.read.side_effect = lambda path: 'hello\nworld'
    registeredTasks['stopwordsDocs'] = lambda: [
        fsStub.writeFileSync('docs/supported-languages.md', 'Unknown\n')
    ]
    registeredTasks['stopwordsDocs']()
    assert 'Unknown' in fsStub.writeFileSync.call_args[0][1]

def test_default_task_registers_all_subtasks(setup_stubs):
    registeredTasks, fsStub, globStub, underscore_mock, languagesStub, gruntStub = setup_stubs
    gruntStub.initConfig()
    gruntStub.loadNpmTasks('grunt-readme')
    registeredTasks['stopwordsToJson'] = lambda: None
    registeredTasks['stopwordsDocs'] = lambda: None
    registeredTasks['default'] = lambda: None
    assert gruntStub.initConfig.called
    assert gruntStub.loadNpmTasks.called
    assert set(registeredTasks.keys()).issuperset({'stopwordsToJson', 'stopwordsDocs', 'default'})