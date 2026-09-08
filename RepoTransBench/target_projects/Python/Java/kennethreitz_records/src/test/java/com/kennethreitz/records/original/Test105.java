package com.kennethreitz.records.original;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class Test105 {

    private Database db;

    @BeforeEach
    public void setup() {
        db = TestDatabaseHelper.createMemoryDatabase();
        db.query("CREATE TABLE foo (a integer)");
    }

    @Test
    public void testIssue105() {
        int result = db.query("select count(*) as n from foo").scalar();
        assertEquals(0, result);
    }
}