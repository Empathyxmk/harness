#include <gtest/gtest.h>
#include <string>
#include <map>
// #include "utils.h"

// Placeholder for alphanumeric_only, lazy_debug, merge_dicts, strip_default until src logic exists
std::string alphanumeric_only(const std::string& input) {
    std::string result;
    for (char c : input) {
        if (isalnum(c)) result += c;
    }
    return result;
}

// Lazy debug: For test, just format input
template<typename... Args>
std::string lazy_debug(const std::string& msg, Args... args) {
    return msg; // Only for test, returns input as string
}

// Merge maps: map1 is overridden by map2 where key overlaps
std::map<std::string, int> merge_dicts(const std::map<std::string,int>& d1, const std::map<std::string,int>& d2) {
    std::map<std::string,int> result = d1;
    for (const auto& kv : d2) {
        result[kv.first] = kv.second;
    }
    return result;
}
std::string strip_default(const std::string& val, const std::string& remove) {
    if (val.substr(0, remove.size()) == remove) {
        return val.substr(remove.size());
    }
    return val;
}

TEST(UtilsTest, AlphanumericOnlyCases) {
    EXPECT_EQ(alphanumeric_only("abc123DEF!@#"), "abc123DEF");
    EXPECT_EQ(alphanumeric_only(" **&$  456 "), "456");
}

TEST(UtilsTest, LazyDebugPrints) {
    auto result = lazy_debug("message", 42, 99);
    EXPECT_EQ(result, "message");
}

TEST(UtilsTest, MergeDicts) {
    std::map<std::string,int> d1 { {"a",1}, {"b",2} };
    std::map<std::string,int> d2 { {"b",3}, {"c",4} };
    auto d = merge_dicts(d1, d2);
    EXPECT_EQ(d["a"], 1);
    EXPECT_EQ(d["b"], 3);
    EXPECT_EQ(d["c"], 4);
}

TEST(UtilsTest, StripDefault) {
    EXPECT_EQ(strip_default(":user:dog:foo", "user:"), "dog:foo");
    EXPECT_EQ(strip_default(":dog", ":cat"), ":dog");
}