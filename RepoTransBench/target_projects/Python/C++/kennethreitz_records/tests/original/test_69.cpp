#include <gtest/gtest.h>
#include "records.hpp"

TEST(Test69, Issue69) {
    records::Database db("sqlite:///:memory:");
    db.query("CREATE table users (id text)");
    db.query("SELECT * FROM users WHERE id = :user", {{"user", std::string("Te'ArnaLambert")}});
    // No assertion, just ensure no error on oddly named param
}