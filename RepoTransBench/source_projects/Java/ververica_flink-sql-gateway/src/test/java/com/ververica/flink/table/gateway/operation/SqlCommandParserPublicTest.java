package com.ververica.flink.table.gateway.operation;

import org.junit.jupiter.api.Test;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

public class SqlCommandParserPublicTest {
    @Test
    public void testPublicParseUseDatabaseCommand() {
        Optional<SqlCommandParser.SqlCommandCall> call = SqlCommandParser.parse("USE `test_public_db`;");
        assertTrue(call.isPresent());
        assertEquals(SqlCommandParser.SqlCommand.USE, call.get().command);
        assertArrayEquals(new String[]{"test_public_db"}, call.get().operands);
    }

    @Test
    public void testPublicParseWrongCommand() {
        Optional<SqlCommandParser.SqlCommandCall> call = SqlCommandParser.parse("MAKE TABLE foobar;");
        assertFalse(call.isPresent());
    }
}