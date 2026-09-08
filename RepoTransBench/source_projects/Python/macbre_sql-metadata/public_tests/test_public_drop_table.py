from sql_metadata import Parser
from sql_metadata.keywords_lists import QueryType


def test_public_drop_table():
    parser = Parser("DROP TABLE bar")
    assert parser.query_type == QueryType.DROP
    assert parser.tables == ["bar"]
    assert parser.columns == []