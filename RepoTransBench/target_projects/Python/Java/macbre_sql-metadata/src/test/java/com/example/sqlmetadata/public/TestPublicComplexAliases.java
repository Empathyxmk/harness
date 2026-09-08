package com.example.sqlmetadata.public;

import com.example.sqlmetadata.Parser;
import org.junit.jupiter.api.Test;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Translated from public_tests/test_public_complex_aliases.py
 */
public class TestPublicComplexAliases {

    @Test
    public void testPublicComplexQueryAliases() {
        String query = """
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
        """;
        Parser parser = new Parser(query);
        Map<String, String> expectedAliases = new HashMap<>();
        expectedAliases.put("X", "source_db.table_x");
        expectedAliases.put("Y", "source_db.table_y");
        expectedAliases.put("subq", "source_db.table_z");
        assertEquals(expectedAliases, parser.getTablesAliases());
        List<String> expectedTables = List.of("source_db.table_x", "source_db.table_y", "source_db.table_z");
        assertEquals(expectedTables, parser.getTables());
    }
}