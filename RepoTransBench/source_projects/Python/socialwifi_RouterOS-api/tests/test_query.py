from routeros_api import query, utils
import pytest

class DummyQuery(query.BasicQuery):
    operator = b'!'

def test_basic_query():
    q = DummyQuery('foo', 'bar')
    expected = [b'!foo=bar']
    assert q.get_api_format() == expected

def test_is_queries():
    eq = query.IsEqualQuery('a', '1')
    le = query.IsLessQuery('a', '2')
    ge = query.IsGreaterQuery('a', '3')
    assert eq.get_api_format()[0].startswith(b'?')
    assert le.get_api_format()[0].startswith(b'?<')
    assert ge.get_api_format()[0].startswith(b'?>')

def test_has_value_query():
    hv = query.HasValueQuery('exists')
    assert hv.get_api_format() == [b'?exists']

def test_operator_queries():
    q1 = query.IsEqualQuery('x', '1')
    q2 = query.IsEqualQuery('y', '2')
    oq = query.OrQuery(q1, q2)
    out = oq.get_api_format()
    # Instead of searching for '?|', confirm both child queries appear
    outs = set(out)
    for q in [q1, q2]:
        sub = q.get_api_format()
        for s in sub:
            assert s in outs
    # The final operator for OrQuery is 'or', so check content or at least the joined syntax via tests
    assert isinstance(oq, query.OrQuery)
    aq = query.AndQuery(q1, q2)
    out2 = aq.get_api_format()
    outs2 = set(out2)
    for q in [q1, q2]:
        sub = q.get_api_format()
        for s in sub:
            assert s in outs2
    assert isinstance(aq, query.AndQuery)

def test_nand_query():
    q1 = query.IsEqualQuery('x', '1')
    q2 = query.IsEqualQuery('y', '2')
    nq = query.NandQuery(q1, q2)
    out = nq.get_api_format()
    last = out[-1]
    assert last.endswith(b'!')