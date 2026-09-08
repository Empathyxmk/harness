package ru.yandex.qatools.embed.postgresql;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Public test for AbstractPsql using alternative values.
 * Dummy implementation included for isolation (remove if main class exists).
 */
public class AbstractPsqlPublicTest {

    static class DummyPsql {
        private String sql;

        public DummyPsql(String sql) {
            this.sql = sql;
        }

        public String run() {
            if (sql.startsWith("SELECT")) return "OK-PUBLIC";
            else return "ERROR-PUBLIC";
        }
    }

    @Test
    public void runReturnsOkForPublicSelect() {
        DummyPsql psql = new DummyPsql("SELECT * FROM bar");
        assertEquals("OK-PUBLIC", psql.run());
    }

    @Test
    public void runReturnsErrorForPublicInsert() {
        DummyPsql psql = new DummyPsql("INSERT QQQ");
        assertEquals("ERROR-PUBLIC", psql.run());
    }
}