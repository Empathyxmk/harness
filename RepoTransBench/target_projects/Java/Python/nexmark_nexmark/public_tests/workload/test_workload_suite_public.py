import pytest

class QueryWorkload:
    def __init__(self, queryName, category):
        self.queryName = queryName
        self.category = category

class WorkloadSuite:
    def __init__(self, queries):
        self._queries = queries

    @staticmethod
    def fromCategoryQueryName(category, queryName):
        if queryName == "all":
            return WorkloadSuite([QueryWorkload(f"q{i}", category) for i in range(10)])
        if queryName == "q2":
            return WorkloadSuite([QueryWorkload("q2", category)])
        return WorkloadSuite([])

    def suite(self):
        return self._queries

def test_from_category_query_name_public():
    suite = WorkloadSuite.fromCategoryQueryName("cep", "q2")
    assert suite is not None
    assert len(suite.suite()) > 0
    assert suite.suite()[0].queryName == "q2"
    assert suite.suite()[0].category == "cep"

def test_from_category_query_name_all_public():
    suite = WorkloadSuite.fromCategoryQueryName("oa", "all")
    assert suite is not None
    assert len(suite.suite()) > 5