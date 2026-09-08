from sql_metadata import keywords_lists as kl

def test_relevant_keywords_and_token_types():
    # Simply check that all lists/sets are non-empty and enums work
    assert "SELECT" in kl.KEYWORDS_BEFORE_COLUMNS
    assert "FROM" in kl.TABLE_ADJUSTMENT_KEYWORDS
    assert "SELECT" in kl.WITH_ENDING_KEYWORDS or "UPDATE" in kl.WITH_ENDING_KEYWORDS
    assert "FROM" in kl.SUBQUERY_PRECEDING_KEYWORDS
    assert kl.COLUMNS_SECTIONS["SELECT"] == "select"
    # Test enums
    assert kl.QueryType.SELECT == "SELECT"
    assert kl.TokenType.COLUMN == "COLUMN"
    # test SUPPORTED_QUERY_TYPES correctly maps
    assert kl.SUPPORTED_QUERY_TYPES["INSERT"] == kl.QueryType.INSERT
    # test all relevant keywords set union contains "LIMIT"
    assert "LIMIT" in kl.RELEVANT_KEYWORDS