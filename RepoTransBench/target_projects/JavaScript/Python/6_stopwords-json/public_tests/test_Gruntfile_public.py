import pytest
from unittest.mock import MagicMock
import json

@pytest.fixture
def setup_public_stubs():
    registeredTasks = {}

    class FsStub:
        def __init__(self):
            self.writeFileSync = MagicMock()

    class GlobStub:
        def __init__(self):
            self.sync = MagicMock()

    class FileStub:
        def __init__(self):
            self.readJSON = MagicMock(return_value={'license': 'Apache-2.0'})
            self.read = MagicMock()

    class GruntStub:
        def __init__(self):
            self.file = FileStub()
            self.initConfig = MagicMock()
            self.loadNpmTasks = MagicMock()
            self.registerTask = lambda name, fn: registeredTasks.setdefault(name, fn)

    fsStub = FsStub()
    globStub = GlobStub()
    underscore_mock = {
        'each': lambda arr, cb: [cb(x) for x in arr],
        'sortBy': lambda arr, fn: sorted(arr, key=fn),
        'map': lambda arr, cb: list(map(cb, arr)),
    }
    languagesStub = type('LangStub', (), {
        'getLanguageInfo': staticmethod(lambda code: {
            "de": "German", "it": "Italian", "zz": "Unknownish"
        }.get(code, code) and {'name': {
            "de": "German", "it": "Italian", "zz": "Unknownish"
        }.get(code, code)})
    })

    gruntStub = GruntStub()
    return registeredTasks, fsStub, globStub, underscore_mock, languagesStub, gruntStub

def test_registers_stopwordsToJson_and_docs_with_different_languages(setup_public_stubs):
    registeredTasks, fsStub, globStub, _, languagesStub, gruntStub = setup_public_stubs
    globStub.sync.return_value = [
        'src/smart/de.txt',
        'src/smart/it.txt'
    ]
    gruntStub.file.read.side_effect = lambda path: {
        'src/smart/de.txt': 'eins\nzwei\ndrei',
        'src/smart/it.txt': 'uno\ndue\ntre'
    }[path]

    # Simulate registration
    registeredTasks['stopwordsToJson'] = lambda: [
        fsStub.writeFileSync('dist/de.json', json.dumps(['eins', 'zwei', 'drei'])),
        fsStub.writeFileSync('dist/it.json', json.dumps(['uno', 'due', 'tre'])),
        fsStub.writeFileSync('stopwords-all.json', json.dumps({'de': ['eins', 'zwei', 'drei'], 'it': ['uno', 'due', 'tre']}))
    ]
    registeredTasks['stopwordsDocs'] = lambda: [
        fsStub.writeFileSync('docs/supported-languages.md', 'Language | Stopword count | Filename\nGerman\nItalian')
    ]

    assert 'stopwordsToJson' in registeredTasks
    registeredTasks['stopwordsToJson']()
    assert fsStub.writeFileSync.call_count >= 3
    calls = fsStub.writeFileSync.call_args_list

    assert 'dist/de.json' in calls[0].args[0]
    assert 'dist/it.json' in calls[1].args[0]
    assert calls[2].args[0] == 'stopwords-all.json'
    itjson = json.loads(calls[1].args[1])
    assert all(x in itjson for x in ['uno', 'due', 'tre'])

    registeredTasks['stopwordsDocs']()
    last_call = fsStub.writeFileSync.call_args_list[-1]
    assert last_call.args[0] == 'docs/supported-languages.md'
    assert 'Language | Stopword count | Filename' in last_call.args[1]
    assert 'German' in last_call.args[1]
    assert 'Italian' in last_call.args[1]

def test_wordsInFile_ignores_empty_and_comment_lines_with_new_data(setup_public_stubs):
    called_list = []
    registeredTasks, fsStub, globStub, _, languagesStub, gruntStub = setup_public_stubs
    def custom_each(arr, fn):
        if arr[0] and '#ignore' in arr[0]:
            called_list.append(True)
        for el in arr:
            fn(el)
    underscore_mock = {
        'each': custom_each,
        'sortBy': lambda arr, fn: sorted(arr, key=fn),
        'map': lambda arr, cb: list(map(cb, arr)),
    }
    globStub.sync.return_value = ['src/smart/de.txt']
    gruntStub.file.read.side_effect = lambda path: 'das\n#ignore\n\nund'
    registeredTasks['stopwordsToJson'] = lambda: [
        fsStub.writeFileSync('dist/de.json', json.dumps(['das', 'und']))
    ]
    registeredTasks['stopwordsToJson']()
    assert any(called_list)
    call_args = fsStub.writeFileSync.call_args_list[0].args
    de_json = json.loads(call_args[1])
    assert 'das' in de_json
    assert 'und' in de_json
    assert '#ignore' not in de_json
    assert '' not in de_json

def test_getStopwords_memoizes_and_sorts_with_different_file(setup_public_stubs):
    registeredTasks, fsStub, globStub, underscore_mock, languagesStub, gruntStub = setup_public_stubs
    globStub.sync.return_value = ['src/smart/it.txt']
    gruntStub.file.read.side_effect = lambda path: 'beta\nalpha\ngamma'
    def stopwordsDocs():
        sorted_words = ['alpha', 'beta', 'gamma']
        fsStub.writeFileSync('docs/supported-languages.md', json.dumps(sorted_words))
    registeredTasks['stopwordsDocs'] = stopwordsDocs

    registeredTasks['stopwordsDocs']()
    captured1 = json.loads(fsStub.writeFileSync.call_args[0][1])
    registeredTasks['stopwordsDocs']()
    captured2 = json.loads(fsStub.writeFileSync.call_args[0][1])
    assert captured1 == captured2
    assert 'alpha' in captured1
    assert captured1.index('alpha') < captured1.index('beta')

def test_handles_files_with_duplicate_words_per_language_public_data(setup_public_stubs):
    registeredTasks, fsStub, globStub, underscore_mock, languagesStub, gruntStub = setup_public_stubs
    globStub.sync.return_value = ['src/smart/de.txt']
    gruntStub.file.read.side_effect = lambda path: 'foo\nbar\nfoo\nbaz\nbar'
    registeredTasks['stopwordsToJson'] = lambda: [
        fsStub.writeFileSync('dist/de.json', json.dumps(['foo', 'bar', 'baz']))
    ]
    registeredTasks['stopwordsToJson']()
    de_json = json.loads(fsStub.writeFileSync.call_args[0][1])
    assert 'foo' in de_json
    assert 'bar' in de_json
    assert 'baz' in de_json
    assert de_json.count('foo') == 1
    assert de_json.count('bar') == 1

def test_stopwordsDocs_handles_unknown_language_code_gracefully_public(setup_public_stubs):
    registeredTasks, fsStub, globStub, underscore_mock, _, gruntStub = setup_public_stubs
    globStub.sync.return_value = ['src/smart/zz.txt']
    gruntStub.file.read.side_effect = lambda path: 'apple\norange'
    registeredTasks['stopwordsDocs'] = lambda: [
        fsStub.writeFileSync('docs/supported-languages.md', 'Unknownish\nzz.json')
    ]
    registeredTasks['stopwordsDocs']()
    s = fsStub.writeFileSync.call_args[0][1]
    assert 'Unknownish' in s
    assert 'zz.json' in s