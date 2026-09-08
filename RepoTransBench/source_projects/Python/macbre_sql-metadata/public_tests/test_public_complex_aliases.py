from sql_metadata import Parser

def test_public_complex_query_aliases():
    query = """
    SELECT
        X.x_id as xid,
        Y.y_value,
        SUM(Z.amount) as total_amount,
        subq.test_val as sub_val
    FROM
        source_db.table_x X
        JOIN source_db.table_y Y ON X.y_id = Y.y_id
        LEFT JOIN (
            SELECT
                ref_id,
                MAX(some_val) as test_val
            FROM source_db.table_z
            GROUP BY ref_id
        ) subq ON X.x_id = subq.ref_id
    WHERE
        Y.active_flag = 1
    GROUP BY
        1, 2, 4
    ORDER BY
        4 DESC
    """
    parser = Parser(query)
    assert parser.tables_aliases == {
        "X": "source_db.table_x",
        "Y": "source_db.table_y",
        "subq": "source_db.table_z",
    }
    assert parser.tables == [
        "source_db.table_x",
        "source_db.table_y",
        "source_db.table_z",
    ]