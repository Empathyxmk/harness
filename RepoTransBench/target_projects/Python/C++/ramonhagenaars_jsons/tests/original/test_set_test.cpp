#include <gtest/gtest.h>
#include <set>
#include <string>
#include <vector>

// Mock datetime string conversion
static std::string datetime_to_iso(const std::tm& dt) {
    char buf[32];
    std::strftime(buf, sizeof(buf), "%Y-%m-%dT%H:%M:%SZ", &dt);
    return std::string(buf);
}

class JsonsSetTest : public ::testing::Test {};

TEST_F(JsonsSetTest, test_dump_set) {
    std::tm dt = {};
    dt.tm_year = 2018 - 1900;
    dt.tm_mon = 7 - 1;
    dt.tm_mday = 8;
    dt.tm_hour = 21;
    dt.tm_min = 34;
    dt.tm_sec = 0;
    std::set<std::string> set_{ datetime_to_iso(dt), datetime_to_iso(dt) };
    std::vector<std::string> dumped(set_.begin(), set_.end());
    std::vector<std::string> expected = { "2018-07-08T21:34:00Z" };
    EXPECT_EQ(dumped, expected);
}

TEST_F(JsonsSetTest, test_load_set) {
    std::string val = "2018-07-08T21:34:00Z";
    std::set<std::string> loaded1 = { val };
    std::set<std::string> loaded2 = { val };
    EXPECT_EQ(loaded1, std::set<std::string>({val}));
    EXPECT_EQ(loaded2, std::set<std::string>({val}));
}