#include <gtest/gtest.h>
#include "sqlitedict.h"
#include <string>
#include <set>
#include <vector>

TEST(PublicCoverageExt, OpenCloseReopen) {
    std::string dbfile = "public_covext_reopen.sqlite";
    {
        SqliteDict d(dbfile, true);
        d.set("foo", "bar");
        d.set("baz", 45);
    }
    SqliteDict d2(dbfile, true);
    EXPECT_EQ(std::get<std::string>(d2.get("foo")), "bar");
    EXPECT_EQ(std::get<int>(d2.get("baz")), 45);
    d2.close();
    remove(dbfile.c_str());
}

TEST(PublicCoverageExt, TableSeparation) {
    std::string dbfile = "public_covext_tabsep.sqlite";
    {
        SqliteDict d1(dbfile, "A", true);
        SqliteDict d2(dbfile, "B", true);
        d1.set("x1", "fooA");
        d2.set("x1", "fooB");
    }
    SqliteDict d1b(dbfile, "A");
    SqliteDict d2b(dbfile, "B");
    EXPECT_EQ(std::get<std::string>(d1b.get("x1")), "fooA");
    EXPECT_EQ(std::get<std::string>(d2b.get("x1")), "fooB");
    d1b.close();
    d2b.close();
    remove(dbfile.c_str());
}

TEST(PublicCoverageExt, BasicSetGetDel_Autocommit) {
    SqliteDict d(":memory:", true);
    d.set("xyz", 678);
    EXPECT_EQ(std::get<int>(d.get("xyz")), 678);
    d.del("xyz");
    EXPECT_FALSE(d.contains("xyz"));
}

TEST(PublicCoverageExt, BasicSetGetDel_NoAutocommit) {
    SqliteDict d(":memory:");
    d.set("xyz", 678);
    EXPECT_EQ(std::get<int>(d.get("xyz")), 678);
    d.del("xyz");
    EXPECT_FALSE(d.contains("xyz"));
}

TEST(PublicCoverageExt, LenAndClear) {
    SqliteDict d(":memory:");
    std::vector<std::string> keys = {"a","b","c","d","e","f"};
    std::vector<int> vals = {10, 11, 12, 13, 14, 15};
    for (size_t i = 0; i < keys.size(); ++i)
        d.set(keys[i], vals[i]);
    EXPECT_EQ(d.len(), 6u);
    d.clear();
    EXPECT_EQ(d.len(), 0u);
}

TEST(PublicCoverageExt, ContainsPopAndKeys) {
    SqliteDict d(":memory:");
    d.set("k1", 333);
    d.set("k2", 444);
    d.set("k3", 555);
    EXPECT_TRUE(d.contains("k1"));
    d.del("k2");
    std::set<std::string> keyset = {"k1","k3"};
    std::vector<std::string> dict_keys;
    for(const auto& item : d.items()) dict_keys.push_back(item.first);
    std::set<std::string> keys_found(dict_keys.begin(), dict_keys.end());
    EXPECT_EQ(keys_found, keyset);
}