#include <gtest/gtest.h>
#include "graphios_backends.h"

TEST(PublicBackends, StripForbiddenChars) {
    EXPECT_EQ(strip_forbidden_chars("a/b:c*d?e<f>g|h"), "abcdefg");
}

TEST(PublicBackends, StripAndLower) {
    EXPECT_EQ(strip_and_lower("AbC-DeF_123"), "abc-def_123");
}

TEST(PublicBackends, StringCleanupTrim) {
    EXPECT_EQ(string_cleanup("   Remove   Spaces   "), "Remove Spaces");
}

TEST(PublicBackends, StringCleanupReplaces) {
    EXPECT_EQ(string_cleanup("strip\tit   now"), "strip it now");
}

TEST(PublicBackends, CamelCaseToUnderscore) {
    EXPECT_EQ(camel_case_to_underscore("PublicCaseToUnderscore"), "public_case_to_underscore");
}

TEST(PublicBackends, StripUnicode) {
    std::string text = "cafe";
    std::string unicodeText = "café 漢字";
    std::string result = strip_unicode(unicodeText);
    EXPECT_TRUE(result.find("cafe") != std::string::npos);
    for (char c : result) EXPECT_LT((unsigned char)c, 128);
}

TEST(PublicBackends, DISABLED_GetattrFromPath) {
    // Python-specific test (dynamic attributes), not directly portable to C++
    SUCCEED();
}