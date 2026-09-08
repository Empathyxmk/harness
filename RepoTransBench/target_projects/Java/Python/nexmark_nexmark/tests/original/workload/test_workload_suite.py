import pytest

class WorkloadSuite:
    def __init__(self, query2workload):
        self._query2workload = query2workload

    def __eq__(self, other):
        return isinstance(other, WorkloadSuite) and self._query2workload == other._query2workload
    def __hash__(self):
        return hash(tuple(sorted(self._query2workload.items())))
    def __str__(self):
        return f"WorkloadSuite(query2Workload={self._query2workload})"
    @staticmethod
    def from_conf(conf, prefix):
        q = conf.get(f"{prefix}.workload.suite.s1.queries", "")
        tps = conf.get(f"{prefix}.workload.suite.s1.tps", "")
        num = conf.get(f"{prefix}.workload.suite.s1.events.num", "")
        suite = dict()
        if q:
            suite[q.split(",")[0]] = {"queries": q, "tps": tps, "events_num": num}
        return WorkloadSuite(suite)
    def get_query_workload(self, query):
        return self._query2workload.get(query)

def test_equals_and_hashcode():
    suite1 = WorkloadSuite({})
    suite2 = WorkloadSuite({})
    assert suite1 == suite2
    assert hash(suite1) == hash(suite2)

def test_to_string():
    suite = WorkloadSuite({})
    assert "query2Workload" in str(suite)

def test_from_conf_returns_suite():
    conf = {
        "nexmark.workload.suite.s1.queries": "q1",
        "nexmark.workload.suite.s1.tps": "1000",
        "nexmark.workload.suite.s1.events.num": "10000"
    }
    suite = WorkloadSuite.from_conf(conf, "nexmark")
    assert suite is not None
    assert suite.get_query_workload("q1") is not None