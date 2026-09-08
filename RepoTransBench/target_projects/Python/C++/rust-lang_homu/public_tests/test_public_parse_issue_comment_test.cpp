#include <gtest/gtest.h>
#include <string>
#include <regex>

std::pair<std::string, std::string> parse_command(const std::string& input) {
    std::regex re(R"(^@homu:\s*([^\s]+)(?:\s+(.*))?$)");
    std::smatch m;
    if (std::regex_match(input, m, re)) {
        std::string cmd = m[1];
        std::string arg = m.size() > 2 ? m[2] : "";
        return {cmd, arg};
    }
    return {"", ""};
}

TEST(PublicParseIssueCommentTest, ParseCommandCustomCase) {
    auto out1 = parse_command("@homu: test-queue");
    EXPECT_EQ(out1.first, "test-queue");
    EXPECT_EQ(out1.second, "");
}

TEST(PublicParseIssueCommentTest, ParseCommandArgumented) {
    auto out2 = parse_command("@homu: clean bar");
    EXPECT_EQ(out2.first, "clean");
    EXPECT_EQ(out2.second, "bar");
}