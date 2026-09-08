#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <algorithm>

namespace pub_utils {

std::string strip_utf8_bom(const std::string& s) {
    static const std::string bom = "\xEF\xBB\xBF";
    if (s.substr(0, 3) == bom) return s.substr(3);
    return s;
}

template<typename T>
std::vector<T> flatten(const std::vector<std::vector<T>>& v) {
    std::vector<T> out;
    for (const auto& inner : v) {
        out.insert(out.end(), inner.begin(), inner.end());
    }
    return out;
}

std::string to_utf8(const std::string& s) {
    return s;
}

std::string remove_last_lf(const std::string& s) {
    if (s.empty()) return s;
    if (s.back() == '\n') return s.substr(0, s.size()-1);
    return s;
}

}

using pub_utils::strip_utf8_bom;
using pub_utils::flatten;
using pub_utils::to_utf8;
using pub_utils::remove_last_lf;

TEST(TestPublicUtils, StripUtf8Bom) {
    std::string s = "\xEF\xBB\xBFAAA";
    ASSERT_EQ(strip_utf8_bom(s), "AAA");
    ASSERT_EQ(strip_utf8_bom("XYZ"), "XYZ");
}

TEST(TestPublicUtils, Flatten) {
    std::vector<std::vector<int>> v = {{1, 2}, {3}};
    auto flat = flatten(v);
    ASSERT_EQ(flat.size(), 3);
    ASSERT_EQ(flat[0], 1);
    ASSERT_EQ(flat[2], 3);
}

TEST(TestPublicUtils, ToUtf8) {
    std::string s = "abc";
    ASSERT_EQ(to_utf8(s), "abc");
}

TEST(TestPublicUtils, RemoveLastLF) {
    ASSERT_EQ(remove_last_lf("aaa\n"), "aaa");
    ASSERT_EQ(remove_last_lf("aaa"), "aaa");
}