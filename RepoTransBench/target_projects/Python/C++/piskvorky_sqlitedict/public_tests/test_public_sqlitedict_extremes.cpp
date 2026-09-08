#include <gtest/gtest.h>
#include "sqlitedict.h"
#include <string>
#include <vector>

TEST(PublicSqliteDictExtremes, SmallAndLargeKeysAndValues) {
    SqliteDict d(":memory:");
    d.set("", std::string("z"));
    EXPECT_EQ(std::get<std::string>(d.get("")), "z");
    std::string key(2000, 'k');
    std::string val(8000, 'v');
    d.set(key, val);
    EXPECT_EQ(std::get<std::string>(d.get(key)), val);
}

TEST(PublicSqliteDictExtremes, LargeNumberOfKeys) {
    SqliteDict d(":memory:");
    const int N = 2117;
    for (int i = 0; i < N; ++i)
        d.set(std::to_string(i), i * 7);
    for (int i = 0; i < N; ++i)
        EXPECT_EQ(std::get<int>(d.get(std::to_string(i))), i * 7);
}

TEST(PublicSqliteDictExtremes, NumericValueTypes) {
    SqliteDict d(":memory:");
    d.set("n1", 1.5);
    d.set("n2", -42);
    d.set("n3", (int)(1<<30));
    d.set("n4", 0);
    EXPECT_EQ(std::get<double>(d.get("n1")), 1.5);
    EXPECT_EQ(std::get<int>(d.get("n2")), -42);
    EXPECT_EQ(std::get<int>(d.get("n3")), (1<<30));
    EXPECT_EQ(std::get<int>(d.get("n4")), 0);
}

TEST(PublicSqliteDictExtremes, UnicodeAndBinary) {
    SqliteDict d(":memory:");
    std::string k = u8"unicø∂e";
    std::string v = u8"välues💡";
    d.set(k, v);
    EXPECT_EQ(std::get<std::string>(d.get(k)), v);
    std::vector<uint8_t> bin_k = {0xff, 0xfe, 0xfd};
    std::vector<uint8_t> bin_v = {0x00, 0x01, 0x02};
    d.set(std::string(bin_k.begin(), bin_k.end()), std::string(bin_v.begin(), bin_v.end()));
    EXPECT_EQ(std::get<std::string>(d.get(std::string(bin_k.begin(), bin_k.end()))), std::string(bin_v.begin(), bin_v.end()));
}

TEST(PublicSqliteDictExtremes, TempDbPersistence) {
    std::string dbfile = "test_public_extreme_tempdb.sqlite";
    {
        SqliteDict d(dbfile, true);
        d.set("foo", "bar");
        d.set("baz", "1,2,3");
    }
    SqliteDict d2(dbfile);
    EXPECT_EQ(std::get<std::string>(d2.get("foo")), "bar");
    EXPECT_EQ(std::get<std::string>(d2.get("baz")), "1,2,3");
    d2.close();
    remove(dbfile.c_str());
}