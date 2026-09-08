#include <gtest/gtest.h>
#include <string>
#include <algorithm>
#include <cctype>

namespace PublicUtils {
inline std::string to_upper(const std::string& s) {
    std::string out = s;
    std::transform(out.begin(), out.end(), out.begin(), [](unsigned char c){ return std::toupper(c); });
    return out;
}
inline bool starts_with(const std::string& s, const std::string& prefix) {
    return s.size() >= prefix.size() && s.compare(0, prefix.size(), prefix) == 0;
}
}

TEST(PublicUtilsTest, ToUpperWorks) {
    EXPECT_EQ(PublicUtils::to_upper("abc-123"), "ABC-123");
    EXPECT_EQ(PublicUtils::to_upper("XYZ"), "XYZ");
}

TEST(PublicUtilsTest, StartsWithWorks) {
    EXPECT_TRUE(PublicUtils::starts_with("picklepete", "pick"));
    EXPECT_FALSE(PublicUtils::starts_with("pyicloud", "icloud"));
}