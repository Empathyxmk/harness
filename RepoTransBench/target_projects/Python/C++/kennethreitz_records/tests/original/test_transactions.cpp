#include <gtest/gtest.h>
#include "records.hpp"
#include "conftest.hpp"

// This set of tests reproduces tests/test_transactions.py in C++ with Google Test.

// Manipulate database by db.query without transactions (plain)
TEST_F(FooTableFixture, TestPlainDb) {
    db.query("INSERT INTO foo VALUES (42)");
    db.query("INSERT INTO foo VALUES (43)");
    auto res = db.query("SELECT count(*) AS n FROM foo");
    // Simulate Python [0].n; for C++, just check scalar
    EXPECT_EQ(res.scalar(), 2);
}

// Manipulate database by conn.query without transactions
TEST_F(FooTableFixture, TestPlainConn) {
    auto conn = db.get_connection();
    conn.query("INSERT INTO foo VALUES (42)");
    conn.query("INSERT INTO foo VALUES (43)");
    auto res = conn.query("SELECT count(*) AS n FROM foo");
    EXPECT_EQ(res.scalar(), 2);
    conn.close();
}

// Failing transaction, self managed
TEST_F(FooTableFixture, TestFailingTransactionSelfManaged) {
    auto conn = db.get_connection();
    auto tx = conn.transaction();
    try {
        conn.query("INSERT INTO foo VALUES (42)");
        conn.query("INSERT INTO foo VALUES (43)");
        throw std::runtime_error("simulated failure");
        tx.commit();
        conn.query("INSERT INTO foo VALUES (44)");
    } catch (const std::runtime_error&) {
        tx.rollback();
    }
    conn.close();
    auto res = db.query("SELECT count(*) AS n FROM foo");
    EXPECT_EQ(res.scalar(), 0);
}

// Failing transaction (with context)
TEST_F(FooTableFixture, TestFailingTransaction) {
    try {
        auto conn = db.transaction();
        conn.query("INSERT INTO foo VALUES (42)");
        conn.query("INSERT INTO foo VALUES (43)");
        throw std::runtime_error("simulated failure");
    } catch (const std::runtime_error&) {
        // Transaction rolled back
    }
    auto res = db.query("SELECT count(*) AS n FROM foo");
    EXPECT_EQ(res.scalar(), 0);
}

// Passing transaction, self managed
TEST_F(FooTableFixture, TestPassingTransactionSelfManaged) {
    auto conn = db.get_connection();
    auto tx = conn.transaction();
    conn.query("INSERT INTO foo VALUES (42)");
    conn.query("INSERT INTO foo VALUES (43)");
    tx.commit();
    conn.close();
    auto res = db.query("SELECT count(*) AS n FROM foo");
    EXPECT_EQ(res.scalar(), 2);
}

// Passing transaction (with context manager style block)
TEST_F(FooTableFixture, TestPassingTransaction) {
    {
        auto conn = db.transaction();
        conn.query("INSERT INTO foo VALUES (42)");
        conn.query("INSERT INTO foo VALUES (43)");
        // Transaction auto-commit on scope end if no error
    }
    auto res = db.query("SELECT count(*) AS n FROM foo");
    EXPECT_EQ(res.scalar(), 2);
}