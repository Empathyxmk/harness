import pytest
from pynubank.nubank import Nubank

def test_find_url_none_public():
    nu = Nubank()
    # Call with unknown keys
    links = {'totally_different': {"href": "https://none-public.local"}}
    assert nu._find_url(['unfindable1','unfindable2'], links) is None

def test_make_graphql_request_post_called_public(monkeypatch):
    class DummyClient:
        def __init__(self):
            self.called = False
            self.args = None
        def post(self, query_url, json):
            self.called = True
            self.args = (query_url, json)
            return "success"
    nu = Nubank(client=DummyClient())
    nu._query_url = "https://graphql-public"
    def dummy_prepare_request_body(obj, variables=None):
        return {"key": "val", "obj": obj, "vars": variables}
    import pynubank.utils.graphql as graphql_mod
    monkeypatch.setattr(graphql_mod, "prepare_request_body", dummy_prepare_request_body)
    out = nu._make_graphql_request("SOMEQUERYPUBLIC", variables={"id": 123})
    assert out == "success"
    assert nu._client.called
    assert isinstance(nu._client.args[1], dict)