#include <gtest/gtest.h>
#include <string>
#include <algorithm>

bool pr_body_contains(const std::string& body, const std::string& key) {
    return body.find(key) != std::string::npos;
}

TEST(PublicPrBodyTest, PrBodyContainsDiffKey) {
    std::string body = "Closes #99\nExtra: refactor code";
    EXPECT_TRUE(pr_body_contains(body, "refactor"));
}

TEST(PublicPrBodyTest, PrBodyNotContainsDiffKey) {
    std::string body = "Implements feature X.\nNone found.";
    EXPECT_FALSE(pr_body_contains(body, "security"));
}