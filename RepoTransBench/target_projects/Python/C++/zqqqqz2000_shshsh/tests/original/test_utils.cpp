#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <algorithm>

namespace shshsh {
namespace utils {

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
    return s; // C++ strings are assumed to be utf-8 here.
}

std::string remove_last_lf(const std::string& s) {
    if (s.empty()) return s;
    if (s.back() == '\n') return s.substr(0, s.size()-1);
    return s;
}

} // namespace utils
} // namespace shshsh

using shshsh::utils::strip_utf8_bom;
using shshsh::utils::flatten;
using shshsh::utils::to_utf8;
using shshsh::utils::remove_last_lf;

TEST(TestUtils, StripUtf8Bom) {
    std::string s = "\xEF\xBB\xBFAAA";
    ASSERT_EQ(strip_utf8_bom(s), "AAA");
    ASSERT_EQ(strip_utf8_bom("XYZ"), "XYZ");
}

TEST(TestUtils, Flatten) {
    std::vector<std::vector<int>> v = {{1, 2}, {3}};
    auto flat = flatten(v);
    ASSERT_EQ(flat.size(), 3);
    ASSERT_EQ(flat[0], 1);
    ASSERT_EQ(flat[2], 3);
}

TEST(TestUtils, ToUtf8) {
    std::string s = "abc";
    ASSERT_EQ(to_utf8(s), "abc");
}

TEST(TestUtils, RemoveLastLF) {
    ASSERT_EQ(remove_last_lf("aaa\n"), "aaa");
    ASSERT_EQ(remove_last_lf("aaa"), "aaa");
}