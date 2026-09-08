#include <gtest/gtest.h>
#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include "syntax_lint.h"

// Helper for test case construction
static std::map<std::string, std::string> make_tag(
        const std::string& summary, 
        const std::string& content,
        int start, int end,
        const std::string& filename
    ) {
    std::map<std::string, std::string> tag;
    tag["summary"] = summary;
    tag["content"] = content;
    tag["start"] = std::to_string(start);
    tag["end"] = std::to_string(end);
    tag["filename"] = filename;
    return tag;
}

TEST(TestParseTagsPublic, EmptyFilePublic) {
    auto res = parse_tags({}, "public_empty.md");
    EXPECT_EQ(res.size(), 0u);
}

TEST(TestParseTagsPublic, SingleValidDetailBlockPublic) {
    std::vector<std::string> lines = {
        "<details>",
        "<summary>This is a new public summary</summary>",
        "Public content goes here.",
        "</details>",
    };
    auto result = parse_tags(lines, "file_public.md");
    ASSERT_EQ(result.size(), 1u);
    EXPECT_EQ(result[0]["summary"], "This is a new public summary");
    EXPECT_EQ(result[0]["content"], "Public content goes here.");
    EXPECT_EQ(result[0]["start"], "0");
    EXPECT_EQ(result[0]["end"], "3");
    EXPECT_EQ(result[0]["filename"], "file_public.md");
}

TEST(TestParseTagsPublic, DetailBlockMissingEndPublic) {
    std::vector<std::string> lines = {
        "<details>",
        "<summary>Public missing close</summary>",
        "Some content"
    };
    auto result = parse_tags(lines, "public_missingend.md");
    EXPECT_EQ(result.size(), 0u); // missing </details>
}

TEST(TestParseTagsPublic, MultipleBlocksWithInvalidOnePublic) {
    std::vector<std::string> lines = {
        "<details>",
        "<summary>Block A</summary>",
        "Alpha content.",
        "</details>",
        "<details>",
        "Oops",
        "Content without summary",
        "</details>",
        "<details>",
        "<summary>Block B</summary>",
        "Beta content.",
        "</details>",
    };
    auto result = parse_tags(lines, "multi_public.md");
    ASSERT_EQ(result.size(), 2u);
    EXPECT_EQ(result[0]["summary"], "Block A");
    EXPECT_EQ(result[1]["summary"], "Block B");
}

TEST(TestParseTagsPublic, DetailBlockWithContentPublic) {
    std::vector<std::string> lines = {
        "<details>",
        "<summary>Alternate summary</summary>",
        "First public line.",
        "Second public line.",
        "</details>",
    };
    auto result = parse_tags(lines, "cpublic.md");
    ASSERT_FALSE(result.empty());
    EXPECT_EQ(result[0]["content"], "First public line.\nSecond public line.");
}

TEST(TestFormattingChecksPublic, ValidDetailFormatPublic) {
    std::vector<std::map<std::string, std::string>> tags = {
        make_tag("A public summary", "A content detail.", 20, 23, "another_public.md")
    };
    auto res = check_formatting(tags);
    EXPECT_EQ(res.size(), 0u);
}

TEST(TestFormattingChecksPublic, MissingSummaryPublic) {
    std::vector<std::map<std::string, std::string>> tags = {
        make_tag("", "Content that's public and missing summary.", 150, 159, "no_public_summary.md")
    };
    auto errors = check_formatting(tags);
    bool found = false;
    for (const auto& err : errors) {
        if (err.find("missing summary") != std::string::npos ||
            err.find("Missing summary") != std::string::npos)
            found = true;
    }
    EXPECT_TRUE(found);
}

TEST(TestFormattingChecksPublic, MismatchedTagsPublic) {
    std::map<std::string, std::string> tag;
    tag["summary"] = "public fail";
    tag["content"] = "content";
    tag["start"] = "9";
    tag["end"] = "None";
    tag["filename"] = "badtag_public_2.md";

    std::vector<std::map<std::string, std::string>> tags { tag };
    auto errors = check_formatting(tags);
    bool found = false;
    for (const auto& err : errors) {
        std::string lwr = err;
        std::transform(lwr.begin(), lwr.end(), lwr.begin(), ::tolower);
        if (lwr.find("mismatched") != std::string::npos ||
            lwr.find("unterminated") != std::string::npos) {
            found = true;
        }
    }
    EXPECT_TRUE(found);
}