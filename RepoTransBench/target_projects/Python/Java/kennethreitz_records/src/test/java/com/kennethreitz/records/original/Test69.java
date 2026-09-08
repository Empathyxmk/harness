package com.kennethreitz.records.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class Test69 {

    @Test
    public void testIssue69() {
        Database db = TestDatabaseHelper.createMemoryDatabase();
        db.query("CREATE TABLE users (id text)");
        db.query("SELECT * FROM users WHERE id = :user", "user", "Te'ArnaLambert");
        db.close();
    }
}