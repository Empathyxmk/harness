#include <gtest/gtest.h>
#include "sqlitedict.h"
#include <string>
#include <map>

TEST(SqliteDictExtremes, Autocommit) {
    std::string db_file = ":memory:";
    SqliteDict d(db_file, true);
    d.set("foo", 42);
    d.set("bar", 123);
    d.close();
    SqliteDict d2(db_file);
    EXPECT_EQ(std::get<int>(d2.get("foo")), 42);
    EXPECT_EQ(std::get<int>(d2.get("bar")), 123);
    d2.close();
}

TEST(SqliteDictExtremes, ReadFlagAndNFlag) {
    std::string db_file = ":memory:";
    SqliteDict d(db_file);
    d.set("a", 1);
    d.commit();
    d.close();
    SqliteDict d_r(db_file); // (simulates read-flag)
    EXPECT_EQ(std::get<int>(d_r.get("a")), 1);
    d_r.close();
    SqliteDict d_n(":memory:", true); // simulate 'flag=n'
    d_n.set("first", 2);
    d_n.commit();
    EXPECT_EQ(std::get<int>(d_n.get("first")), 2);
    d_n.close();
}

TEST(SqliteDictExtremes, JournalModeOff) {
    std::string db_file = ":memory:";
    SqliteDict d(db_file);
    d.set("x", 1);
    d.commit();
    d.close();
    SqliteDict d2(db_file);
    EXPECT_EQ(std::get<int>(d2.get("x")), 1);
    d2.close();
}

TEST(SqliteDictExtremes, CustomEncodeDecode) {
    SqliteDict d(":memory:");
    std::map<std::string, int> val = {{"a", 1}, {"b", 2}};
    d.set("json", val["a"]);
    EXPECT_EQ(std::get<int>(d.get("json")), 1);
    d.close();
}

TEST(SqliteDictExtremes, OuterStackFalse) {
    SqliteDict d(":memory:");
    d.set("x", 1);
    d.close();
}