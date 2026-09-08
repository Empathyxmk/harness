#include <gtest/gtest.h>
#include <string>
#include <map>
#include <algorithm>

std::map<std::string, std::string> lower_dict(const std::map<std::string, std::string>& in) {
    std::map<std::string, std::string> out;
    for (const auto& pair : in) {
        std::string key = pair.first;
        std::transform(key.begin(), key.end(), key.begin(), ::tolower);
        out[key] = pair.second;
    }
    return out;
}

TEST(PublicUtilTest, PublicLowerDict) {
    std::map<std::string, std::string> upper_dict{
        {"KEY", "10"},
        {"ALPHA", "20"},
        {"Z", "VALUE"},
        {"MiXeD", "Flag"},
        {"foo", "Bar"}
    };
    auto lowered = lower_dict(upper_dict);
    ASSERT_EQ(lowered["key"], "10");
    ASSERT_EQ(lowered["alpha"], "20");
    ASSERT_EQ(lowered["z"], "VALUE");
    ASSERT_EQ(lowered["mixed"], "Flag");
    ASSERT_EQ(lowered["foo"], "Bar");
}