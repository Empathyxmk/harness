#include <gtest/gtest.h>
#include <sqlite3.h>

TEST(Sqlite3Test, InMemoryInsert) {
    sqlite3 *db;
    ASSERT_EQ(sqlite3_open(":memory:", &db), SQLITE_OK);
    char *err = nullptr;
    ASSERT_EQ(sqlite3_exec(db, "CREATE TABLE test_public(id int, name text)", nullptr, nullptr, &err), SQLITE_OK);
    ASSERT_EQ(sqlite3_exec(db, "INSERT INTO test_public(id, name) VALUES (2, 'sqltest')", nullptr, nullptr, &err), SQLITE_OK);

    sqlite3_stmt *stmt;
    ASSERT_EQ(sqlite3_prepare_v2(db, "SELECT id, name FROM test_public", -1, &stmt, nullptr), SQLITE_OK);
    ASSERT_EQ(sqlite3_step(stmt), SQLITE_ROW);
    ASSERT_EQ(sqlite3_column_int(stmt, 0), 2);
    ASSERT_STREQ(reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1)), "sqltest");
    sqlite3_finalize(stmt);
    sqlite3_close(db);
}