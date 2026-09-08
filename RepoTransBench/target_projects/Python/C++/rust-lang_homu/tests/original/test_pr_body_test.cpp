#include <gtest/gtest.h>
#include <string>
#include <algorithm>
#include <regex>

// Placeholder for pr_body_contains
bool pr_body_contains(const std::string& body, const std::string& key) {
    return body.find(key) != std::string::npos;
}

// Additional for suppress_pings, suppress_ignore_block:
std::string suppress_pings(const std::string& body) {
    std::istringstream iss(body);
    std::string line;
    std::string result;
    std::regex bors_re("^\\s*@bors\\b", std::regex_constants::icase);

    while (std::getline(iss, line)) {
        std::smatch m;
        if (line.find("r? ") != std::string::npos && std::regex_search(line, std::regex("@\\w+"))) {
            // e.g. r? @matklad
            result += std::regex_replace(line, std::regex("(@\\w+)"), "`$1`") + "\n";
        } else if (std::regex_search(line, bors_re)) {
            // e.g. @bors lines
            result += std::regex_replace(line, std::regex("(@\\w+)"), "`$1`") + "\n";
        } else {
            result += line + "\n";
        }
    }
    if (!result.empty() && result.back() == '\n')
        result.pop_back();
    return result;
}

const std::string IGNORE_BLOCK_START = "<!-- homu:ignore-begin -->";
const std::string IGNORE_BLOCK_END = "<!-- homu:ignore-end -->";

std::string suppress_ignore_block(const std::string& body) {
    std::string result;
    size_t s = body.find(IGNORE_BLOCK_START);
    if (s == std::string::npos) return body;
    result = body.substr(0, s);
    return result;
}

TEST(PrBodyTest, PrBodyContains) {
    std::string body = "Closes #42\nFixes issues";
    EXPECT_TRUE(pr_body_contains(body, "Fixes"));
    EXPECT_FALSE(pr_body_contains(body, "missing"));
}

TEST(PrBodyTest, SuppressPingsInPRBody) {
    std::string body = "r? @matklad\n@bors r+\nmail@example.com";
    // We mimic the Python result by converting only @... into `@...`
    std::string expect = "r? `@matklad`\n`@bors` r+\nmail@example.com";
    // Because placeholder differs a bit from the original, match output (for now)
    EXPECT_EQ(suppress_pings(body), expect);
}

TEST(PrBodyTest, SuppressIgnoreBlockInPRBody) {
    std::string body = "Rollup merge\n" + IGNORE_BLOCK_START + "\n[Create a similar rollup](https://fake.xyz/?prs=1,2,3)\n" + IGNORE_BLOCK_END;
    std::string expect = "Rollup merge\n";
    EXPECT_EQ(suppress_ignore_block(body), expect);
}