#include <gtest/gtest.h>
#include "fuzzywuzzy/utils.h"
#include "fuzzywuzzy/StringMatcher.h"

TEST(PublicUtilsStringMatcherTest, AsciiDammitPublic) {
    std::string s = "Café Noël Über ß";
    std::string result = fuzzywuzzy::utils::asciidammit(s);
    EXPECT_TRUE(typeid(result) == typeid(std::string));
    EXPECT_EQ(result.find('\u00e9'), std::string::npos);
}
TEST(PublicUtilsStringMatcherTest, AsciiOnlyPublic) {
    std::string s = fuzzywuzzy::utils::asciidammit("façade naïve jalapeño");
    std::string result = fuzzywuzzy::utils::asciionly(s);
    for (char c : result) {
        EXPECT_TRUE(isalnum(c) || c == ' ');
    }
}
TEST(PublicUtilsStringMatcherTest, FullProcessPublic) {
    std::string s = "Fußball & Crème brûlée";
    std::string result = fuzzywuzzy::utils::full_process(s);
    EXPECT_TRUE(typeid(result) == typeid(std::string));
    EXPECT_EQ(result.find("&"), std::string::npos);
}
TEST(PublicUtilsStringMatcherTest, StringMatcherRatioPublic) {
    std::string s1 = "hello";
    std::string s2 = "hullo";
    fuzzywuzzy::StringMatcher m;
    m.set_seq1(s1);
    m.set_seq2(s2);
    double ratio = m.ratio();
    EXPECT_GT(ratio, 0.7);
    EXPECT_LT(ratio, 1.0);
}