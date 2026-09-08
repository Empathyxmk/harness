# coding=utf-8

import collections
import textwrap

import pytest

from honcho import environ


@pytest.mark.parametrize('content,commands', [
    [
        """
        BAR=foo
        """,
        {'BAR': 'foo'}
    ],
    [
        """
        ALPHA=beta
        GAMMA=delta
        """,
        {'ALPHA': 'beta', 'GAMMA': 'delta'}
    ],
    [
        # No newline at EOF
        """
        QUX=baz""",
        {'QUX': 'baz'}
    ],
    [
        # Comments, changed text
        """
        #another comment
        """,
        {}
    ],
    [
        # Invalid, changed
        """
        *item=value
        """,
        {}
    ],
    [
        # Single quoted with different value
        """
        VAR1='hi\\"there'
        """,
        {'VAR1': 'hi\\"there'}
    ],
    [
        # Double quoted, changed contents
        """
        VAR2="bye'now"
        """,
        {'VAR2': "bye'now"}
    ],
    [
        # Quotation mark surrounded, different key
        r"""
        VAR3='"public"'
        """,
        {'VAR3': '"public"'}
    ],
    [
        # Escaped quotation mark, different key
        r"""
        VAR4=\"hello\"
        """,
        {'VAR4': '"hello"'}
    ],
    [
        # At-sign in value, different
        r"""
        EMAIL=another@address.com
        """,
        {'EMAIL': 'another@address.com'}
    ],
    [
        # Different punctuation
        r"""
        MYVAR=!sym#bols^
        """,
        {'MYVAR': '!sym#bols^'}
    ],
    [
        # Other Unicode values
        r"""
        EMOJI=😀🚀🔥
        """,
        {'EMOJI': '😀🚀🔥'}
    ],
    [
        # Quoted space, other variable name
        r"""
        SPACED='another one'
        """,
        {'SPACED': 'another one'}
    ],
    [
        # Escaped chars different
        r"""
        T1='bar\\tbaz'
        T2='baz\\nqux'
        T3='baz\\$qux'
        """,
        {'T1': 'bar\\tbaz',
         'T2': 'baz\\nqux',
         'T3': 'baz\\$qux'}
    ],
])
def test_environ_parse(content, commands):
    content = textwrap.dedent(content)
    result = environ.parse(content)
    assert result == commands


@pytest.mark.parametrize('content,processes', [
    [
        # Simple, changed
        """
        api: runapi
        """,
        {'api': 'runapi'}
    ],
    [
        # Simple 2, changed names
        """
        test: pytest main.py
        build: make all
        """,
        {'test': 'pytest main.py', 'build': 'make all'}
    ],
    [
        # No newline at EOF
        """
        logger: logit""",
        {'logger': 'logit'}
    ],
    [
        # Comments, changed
        """
        #omitted: step
        """,
        {}
    ],
    [
        # Invalid, changed char
        """
        @proc: action
        """,
        {}
    ],
    [
        # Different valid characters in name
        """
        test-task: echo hi
        """,
        {'test-task': 'echo hi'}
    ],
    [
        # Shell metacharacters different
        """
        batch: sh -c "ls -la" >>out.log 2>&1
        """,
        {'batch': 'sh -c "ls -la" >>out.log 2>&1'}
    ],
])
def test_parse_procfile(content, processes):
    content = textwrap.dedent(content)
    p = environ.parse_procfile(content)
    assert p.processes == processes


def test_parse_procfile_ordered():
    content = textwrap.dedent("""
    red: apple
    green: pear
    blue: berry
    yellow: lemon
    """)

    p = environ.parse_procfile(content)
    order = [k for k in p.processes]
    assert order == ['red', 'green', 'blue', 'yellow']


class TestProcfile(object):
    def test_has_no_processes_after_init(self):
        p = environ.Procfile()
        assert len(p.processes) == 0

    def test_add_process(self):
        p = environ.Procfile()
        p.add_process('bar', 'echo 456')
        assert 'echo 456' == p.processes['bar']

    def test_add_process_ensures_unique_name(self):
        p = environ.Procfile()
        p.add_process('bar', 'echo 456')
        with pytest.raises(AssertionError):
            p.add_process('bar', 'echo 456')


def ep(*args, **kwargs):
    return environ.expand_processes(collections.OrderedDict(args), **kwargs)


def test_expand_processes_name():
    p = ep(("alpha", "command a"))
    assert len(p) == 1
    assert p[0].name == "alpha.1"


def test_expand_processes_name_multiple():
    p = ep(("alpha", "command a"), ("beta", "command b"))
    assert len(p) == 2
    assert p[0].name == "alpha.1"
    assert p[1].name == "beta.1"


def test_expand_processes_name_concurrency():
    p = ep(("alpha", "command a"), concurrency={"alpha": 2})
    assert len(p) == 2
    assert p[0].name == "alpha.1"
    assert p[1].name == "alpha.2"


def test_expand_processes_name_concurrency_multiple():
    p = ep(("alpha", "command a"), ("beta", "command b"),
           concurrency={"alpha": 2, "beta": 3})
    assert len(p) == 5
    assert p[0].name == "alpha.1"
    assert p[1].name == "alpha.2"
    assert p[2].name == "beta.1"
    assert p[3].name == "beta.2"
    assert p[4].name == "beta.3"


def test_expand_processes_command():
    p = ep(("test", "run tests"))
    assert p[0].cmd == "run tests"


def test_expand_processes_port_not_defaulted():
    p = ep(("random", "something else"))
    assert "PORT" not in p[0].env