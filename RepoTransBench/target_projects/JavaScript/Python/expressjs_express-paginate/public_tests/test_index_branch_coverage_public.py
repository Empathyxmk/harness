import pytest
from src.express_paginate import href, hasNextPages, getArrayPages, middleware

def reqres_req(data=None):
    class DummyReq:
        def __init__(self, d):
            self.query = dict(d['query']) if d and 'query' in d else {}
            self.originalUrl = d.get('originalUrl', '') if d else ''
            self.skip = 0
            self.offset = 0
    return DummyReq(data) if data else DummyReq({'query': {}})

def reqres_res():
    class DummyRes:
        def __init__(self):
            self.locals = type('Locals', (), {})()
            self.locals.paginate = type('Paginate', (), {})()
    return DummyRes()

class TestExpressPaginateBranchCoveragePublic:
    # .href
    def test_href_clamps_page_to_1_if_prev_true_from_page_2(self):
        req = type('Req', (), {'originalUrl': '/bar', 'query': {'page': '2'}})()
        href_fn = href(req)
        out = href_fn(True)
        assert 'page=1' in out

    def test_href_adds_params_even_when_not_object(self):
        req = type('Req', (), {'originalUrl': '/bar', 'query': {'page': '5'}})()
        href_fn = href(req)
        out_undefined = href_fn(False, None)
        assert 'page=6' in out_undefined
        out_null = href_fn(False, None)
        assert 'page=6' in out_null

    # .hasNextPages
    def test_hasnextpages_throws_if_pagecount_negative(self):
        req = type('Req', (), {'query': {'page': 2}})()
        with pytest.raises(Exception, match=r'not a number >= 0'):
            hasNextPages(req)(-3)

    def test_hasnextpages_throws_if_pagecount_not_a_number(self):
        req = type('Req', (), {'query': {'page': 2}})()
        with pytest.raises(Exception, match=r'not a number'):
            hasNextPages(req)("abc")

    def test_hasnextpages_handles_zero_pages(self):
        req = type('Req', (), {'query': {'page': 2}})()
        result = hasNextPages(req)(0)
        assert result is False

    # .getArrayPages
    def mkreq(self):
        return type('Req', (), {'originalUrl': '/baz', 'query': {'page': 7}})()

    def test_getarraypages_throws_if_currentpage_not_a_number(self):
        req = self.mkreq()
        with pytest.raises(Exception, match=r'currentPage'):
            getArrayPages(req)(4, 20, 'foo')
        with pytest.raises(Exception, match=r'currentPage'):
            getArrayPages(req)(4, 20, -5)

    def test_getarraypages_throws_if_pagecount_invalid(self):
        req = self.mkreq()
        with pytest.raises(Exception, match=r'pageCount'):
            getArrayPages(req)(2, -2, 1)
        with pytest.raises(Exception, match=r'pageCount'):
            getArrayPages(req)(2, "bar", 1)

    def test_getarraypages_throws_if_limit_invalid(self):
        req = self.mkreq()
        with pytest.raises(Exception, match=r'limit'):
            getArrayPages(req)(-5, 5, 1)
        with pytest.raises(Exception, match=r'limit'):
            getArrayPages(req)("baz", 5, 1)

    def test_getarraypages_defaults_limit_and_gives_range(self):
        req = self.mkreq()
        arr = getArrayPages(req)(None, 30, 7)
        assert isinstance(arr, list)
        assert len(arr) == 3
        assert arr[0]['number'] == 6

    def test_getarraypages_limit_0_returns_full_array(self):
        req = self.mkreq()
        arr = getArrayPages(req)(0, 15, 5)
        assert isinstance(arr, list)
        assert len(arr) > 0

    # .middleware
    def test_middleware_defaults_params(self):
        req = reqres_req({'query': {}})
        res = reqres_res()
        done_called = [False]
        def _done():
            done_called[0] = True
        middleware()(req, res, _done)
        assert req.query['page'] == 1
        assert req.query['limit'] == 10
        assert res.locals.paginate.hasPreviousPages is False
        assert callable(res.locals.paginate.href)
        assert callable(res.locals.paginate.hasNextPages)
        assert callable(res.locals.paginate.getArrayPages)
        assert done_called[0]

    def test_middleware_clamp_limit_to_maxlimit(self):
        req = reqres_req({'query': {'limit': '100', 'page': '3'}})
        res = reqres_res()
        done_called = [False]
        def _done():
            done_called[0] = True
        middleware(7, 9)(req, res, _done)
        assert req.query['limit'] == 9
        assert done_called[0]

    def test_middleware_clamp_negative_limit(self):
        req = reqres_req({'query': {'limit': '-10'}})
        res = reqres_res()
        done_called = [False]
        def _done():
            done_called[0] = True
        middleware()(req, res, _done)
        assert req.query['limit'] == 0
        assert done_called[0]

    def test_middleware_clamp_negative_page(self):
        req = reqres_req({'query': {'page': '-12'}})
        res = reqres_res()
        done_called = [False]
        def _done():
            done_called[0] = True
        middleware()(req, res, _done)
        assert req.query['page'] == 1
        assert done_called[0]

    def test_middleware_non_string_page_limit(self):
        req = reqres_req({'query': {'page': 5, 'limit': 12}})
        res = reqres_res()
        done_called = [False]
        def _done():
            done_called[0] = True
        middleware()(req, res, _done)
        assert req.query['page'] == 1
        assert req.query['limit'] == 10
        assert done_called[0]

    def test_middleware_skip_offset_computation(self):
        req = reqres_req({'query': {'page': '4', 'limit': '7'}})
        res = reqres_res()
        done_called = [False]
        def _done():
            done_called[0] = True
        middleware()(req, res, _done)
        assert req.skip == 21
        assert req.offset == 21
        assert done_called[0]