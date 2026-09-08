#pragma once
#include "records.hpp"
#include <string>

// This header provides C++ test fixture helpers inspired by the original Python pytest fixtures.

struct TestDB {
    // This is a test helper to simulate the 'db' fixture.
    records::Database db;
    TestDB() : db("sqlite:///:memory:") {}
    ~TestDB() { db.close(); }
};

struct FooTableFixture : public ::testing::Test {
    records::Database db;
    FooTableFixture() : db("sqlite:///:memory:") {}

    void SetUp() override {
        db.query("CREATE TABLE foo (a integer)");
    }
    void TearDown() override {
        db.query("DROP TABLE foo");
        db.close();
    }
};