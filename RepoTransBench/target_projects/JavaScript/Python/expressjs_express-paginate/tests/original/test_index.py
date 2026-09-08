import pytest
from src.express_paginate import href, hasNextPages, middleware, getArrayPages

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

class TestHref:
    @pytest.fixture(autouse=True)
    def _setup(self):
        self.req = type('Req', (), {
            'originalUrl': 'http://niftylettuce.com/',
            'query': {'page': 3}
        })()

    def test_return_function(self):
        result = href(self.req)
        assert callable(result)

    def test_next_page_when_invoked_no_args(self):
        import urllib.parse
        result = href(self.req)()
        expected_url = '{}?page={}'.format(urllib.parse.urlparse(self.req.originalUrl).path, self.req.query['page'] + 1)
        assert result == expected_url

    def test_next_page_when_false(self):
        import urllib.parse
        result = href(self.req)(False)
        expected_url = '{}?page={}'.format(urllib.parse.urlparse(self.req.originalUrl).path, self.req.query['page'] + 1)
        assert result == expected_url

    def test_prev_page_href_when_true(self):
        import urllib.parse
        result = href(self.req)(True)
        expected_url = '{}?page={}'.format(urllib.parse.urlparse(self.req.originalUrl).path, self.req.query['page'] - 1)
        assert result == expected_url

    def test_prev_page_href_and_sorted_by_title(self):
        import urllib.parse
        result = href(self.req)(True, {'sort': 'title'})
        expected_url = '{}?page={}&sort=title'.format(urllib.parse.urlparse(self.req.originalUrl).path, self.req.query['page'] - 1)
        assert result == expected_url

    def test_next_page_href_and_sorted_by_title(self):
        import urllib.parse
        result = href(self.req)(False, {'sort': 'title'})
        expected_url = '{}?page={}&sort=title'.format(urllib.parse.urlparse(self.req.originalUrl).path, self.req.query['page'] + 1)
        assert result == expected_url

    def test_current_page_sorted_by_title(self):
        import urllib.parse
        result = href(self.req)({'sort': 'title'})
        expected_url = '{}?page={}&sort=title'.format(urllib.parse.urlparse(self.req.originalUrl).path, self.req.query['page'])
        assert result == expected_url

class TestHasNextPages:
    @pytest.fixture(autouse=True)
    def _setup(self):
        self.req = type('Req', (), {'query': {'page': 3}})()

    def test_returns_function(self):
        fn = hasNextPages(self.req)
        assert callable(fn)

    def test_returns_true_when_more_pages(self):
        fn = hasNextPages(self.req)
        assert fn(4) is True

    def test_returns_false_when_no_more_pages(self):
        fn = hasNextPages(self.req)
        assert fn(3) is False

    def test_throws_when_pagecount_not_a_number(self):
        fn = hasNextPages(self.req)
        with pytest.raises(Exception, match=r'not a number'):
            fn('')

    def test_throws_when_pagecount_less_than_zero(self):
        fn = hasNextPages(self.req)
        with pytest.raises(Exception, match=r'>= 0'):
            fn('')

class TestMiddlewarePureFunction:
    def test_successive_calls_do_not_mutate(self):
        import threading

        first = middleware(10, 20)
        second = middleware(30, 40)

        results = {}

        def call1():
            req = reqres_req()
            first(req, reqres_res(), lambda err=None: results.update({"call1": req.query["limit"]}))
        def call2():
            req = reqres_req()
            second(req, reqres_res(), lambda err=None: results.update({"call2": req.query["limit"]}))

        t1 = threading.Thread(target=call1)
        t2 = threading.Thread(target=call2)
        t1.start(); t2.start(); t1.join(); t2.join()

        assert results["call1"] == 10
        assert results["call2"] == 30

    def test_maxlimit_in_previous_calls(self):
        import threading

        first = middleware(10, 20)
        second = middleware(30, 40)

        results = {}

        def call1():
            req = reqres_req({'query': {'limit': '100'}})
            first(req, reqres_res(), lambda err=None: results.update({'call1': req.query['limit']}))
        def call2():
            req = reqres_req({'query': {'limit': '100'}})
            second(req, reqres_res(), lambda err=None: results.update({'call2': req.query['limit']}))

        t1 = threading.Thread(target=call1)
        t2 = threading.Thread(target=call2)
        t1.start(); t2.start(); t1.join(); t2.join()

        assert results["call1"] == 20
        assert results["call2"] == 40

    def test_arg_zero_sets_limit_and_page_and_offset_zero(self):
        import threading

        first = middleware(10, 20)
        second = middleware(30, 40)

        checks = []

        def callf(reqfn, limit_val):
            req = reqfn({'query': {'page': '0', 'limit': '0'}})
            return lambda: middleware(limit_val, (20 if limit_val == 10 else 40))(req, reqres_res(),
                lambda err=None: checks.append({'limit': req.query['limit'], 'page': req.query['page'], 
                                                'skip': req.skip, 'offset': req.offset}))

        threads = [
            threading.Thread(target=callf(reqres_req, 10)),
            threading.Thread(target=callf(reqres_req, 30)),
            threading.Thread(target=callf(reqres_req, 10)),  # negative
            threading.Thread(target=callf(reqres_req, 30)),  # negative
            threading.Thread(target=callf(reqres_req, 10)),  # not int
            threading.Thread(target=callf(reqres_req, 30)),  # not int
        ]
        for t in threads: t.start()
        for t in threads: t.join()

        for c in checks:
            assert c['limit'] == 0
            assert c['page'] == 1
            assert c['skip'] == 0
            assert c['offset'] == 0

class TestGetArrayPages:
    def setup_method(self):
        self.req = type('Req', (), {
            'originalUrl': 'http://niftylettuce.com/',
            'query': {'page': 3}
        })()
        self.limit = 5
        self.fakeMaxCount = 10
        self.pages = getArrayPages(self.req)(self.limit, self.fakeMaxCount, self.req.query['page'])

    def test_returns_array_of_pages(self):
        assert isinstance(self.pages, list)

    def test_contains_correct_page_numbers_and_urls(self):
        for idx, p in enumerate(self.pages):
            assert p['number'] == idx + 1
            assert 'page={}'.format(idx + 1) in p['url']

    def test_limit_more_than_total_pages(self):
        for idx, p in enumerate(getArrayPages(self.req)(4, 3, 3)):
            assert p['number'] == idx + 1
            assert 'page={}'.format(idx + 1) in p['url']

    def test_validations(self):
        # negative limit
        with pytest.raises(Exception, match=r'>= 0'):
            getArrayPages(self.req)(-1, self.fakeMaxCount, self.req.query['page'])
        # pageCount is string
        with pytest.raises(Exception, match=r'>= 0'):
            getArrayPages(self.req)(self.limit, '', self.req.query['page'])
        # currentPage is object
        with pytest.raises(Exception, match=r'>= 0'):
            getArrayPages(self.req)(self.limit, self.fakeMaxCount, {})