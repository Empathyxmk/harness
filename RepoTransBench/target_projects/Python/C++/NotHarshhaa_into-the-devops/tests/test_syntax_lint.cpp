#include <gtest/gtest.h>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <cstdio>
#include "syntax_lint.h"

// Helper for byte-to-string conversion for test vectors (Python b"" style lines)
static std::vector<std::string> as_strvec(const std::vector<std::string>& xs) { return xs; }
static std::vector<std::string> as_strvec_bytes(const std::vector<const char*>& xs) {
    std::vector<std::string> result;
    for (auto s : xs) result.push_back(s);
    return result;
}

// Tests for count_details
TEST(TestCountDetails, BalancedDetails) {
    auto lines = as_strvec_bytes({
        "<details>\n",
        "content\n",
        "</details>\n",
    });
    EXPECT_TRUE(count_details(lines));
}

TEST(TestCountDetails, UnbalancedDetailsMoreOpens) {
    auto lines = as_strvec_bytes({
        "<details>\n",
        "stuff\n"
    });
    EXPECT_FALSE(count_details(lines));
}

TEST(TestCountDetails, UnbalancedDetailsMoreCloses) {
    auto lines = as_strvec_bytes({
        "</details>\n",
        "<details>\n",
        "</details>\n"
    });
    EXPECT_FALSE(count_details(lines));
}

// Tests for count_summary
TEST(TestCountSummary, BalancedSummary) {
    auto lines = as_strvec_bytes({
        "<summary>\n",
        "foo\n",
        "</summary>\n"
    });
    EXPECT_TRUE(count_summary(lines));
}

TEST(TestCountSummary, UnbalancedSummaryOpen) {
    auto lines = as_strvec_bytes({
        "<summary>\n",
        "foo\n"
    });
    EXPECT_FALSE(count_summary(lines));
}

TEST(TestCountSummary, UnbalancedSummaryClose) {
    auto lines = as_strvec_bytes({
        "foo\n",
        "</summary>\n"
    });
    EXPECT_FALSE(count_summary(lines));
}

// Tests for check_details_tag
TEST(TestCheckDetailsTag, CorrectNesting) {
    syntax_lint_errors.clear();
    auto lines = as_strvec_bytes({"<details>\n", "text\n", "</details>\n"});
    check_details_tag(lines);
    EXPECT_EQ(syntax_lint_errors.size(), 0u);
}

TEST(TestCheckDetailsTag, MissingClosing) {
    syntax_lint_errors.clear();
    auto lines = as_strvec_bytes({"<details>\n", "<details>\n"});
    check_details_tag(lines);
    bool found = false;
    for (const auto& e : syntax_lint_errors) {
        if (e.find("Missing closing detail") != std::string::npos ||
            e.find("Missing closing detail tag") != std::string::npos)
            found = true;
    }
    EXPECT_TRUE(found);
}

TEST(TestCheckDetailsTag, MissingOpening) {
    syntax_lint_errors.clear();
    auto lines = as_strvec_bytes({"</details>\n"});
    check_details_tag(lines);
    bool found = false;
    for (const auto& e : syntax_lint_errors) {
        if (e.find("Missing opening detail") != std::string::npos)
            found = true;
    }
    EXPECT_TRUE(found);
}

TEST(TestCheckDetailsTag, OnelineDetail) {
    syntax_lint_errors.clear();
    auto lines = as_strvec_bytes({"<details>foo</details>\n"});
    check_details_tag(lines);
    EXPECT_EQ(syntax_lint_errors.size(), 0u);
}

// Tests for check_summary_tag
TEST(TestCheckSummaryTag, CorrectSummary) {
    syntax_lint_errors.clear();
    auto lines = as_strvec_bytes({"<summary>\n", "text\n", "</summary>\n"});
    check_summary_tag(lines);
    EXPECT_EQ(syntax_lint_errors.size(), 0u);
}

TEST(TestCheckSummaryTag, MissingClosing) {
    syntax_lint_errors.clear();
    auto lines = as_strvec_bytes({"<summary>\n", "<summary>\n"});
    check_summary_tag(lines);
    bool found = false;
    for (const auto& e : syntax_lint_errors) {
        if (e.find("Missing closing summary") != std::string::npos)
            found = true;
    }
    EXPECT_TRUE(found);
}

TEST(TestCheckSummaryTag, MissingOpening) {
    syntax_lint_errors.clear();
    auto lines = as_strvec_bytes({"</summary>\n"});
    check_summary_tag(lines);
    bool found = false;
    for (const auto& e : syntax_lint_errors) {
        if (e.find("Missing opening summary") != std::string::npos)
            found = true;
    }
    EXPECT_TRUE(found);
}

TEST(TestCheckSummaryTag, OnelineSummary) {
    syntax_lint_errors.clear();
    auto lines = as_strvec_bytes({"<summary>xyz</summary>\n"});
    check_summary_tag(lines);
    EXPECT_EQ(syntax_lint_errors.size(), 0u);
}

TEST(TestCheckSummaryTag, NestedOpen) {
    syntax_lint_errors.clear();
    auto lines = as_strvec_bytes({"<summary>\n", "<summary>\n"});
    check_summary_tag(lines);
    bool found = false;
    for (const auto& e : syntax_lint_errors) {
        if (e.find("Missing closing summary ") != std::string::npos ||
            e.find("Missing closing summary tag") != std::string::npos)
            found = true;
    }
    EXPECT_TRUE(found);
}

// Test for check_md_file
class CheckMdFileTest : public ::testing::Test {
protected:
    void SetUp() override {
        syntax_lint_errors.clear();
    }
};

TEST_F(CheckMdFileTest, ValidFile) {
    syntax_lint_errors.clear();
    std::string fname = "testtmp_mdfile_valid.md";
    std::ofstream fout(fname, std::ios::binary);
    fout << "<details>\ntext\n<summary>\ntext\n</summary>\n</details>\n";
    fout.close();
    syntax_lint_p = fname;
    check_md_file(fname);
    std::remove(fname.c_str());
    EXPECT_EQ(syntax_lint_errors.size(), 0u);
}

TEST_F(CheckMdFileTest, FileWithErrors) {
    std::string fname = "testtmp_mdfile_err.md";
    std::ofstream fout(fname, std::ios::binary);
    fout << "<details>\nno close\n<summary>\nno close\n";
    fout.close();
    syntax_lint_p = fname;
    syntax_lint_errors.clear();
    check_md_file(fname);
    std::remove(fname.c_str());
    EXPECT_TRUE(!syntax_lint_errors.empty()); // should be a list/vector
}

// Simulate the main-guard (execution)
TEST(TestMainGuard, MainBlock) {
    // GOOD file (exit should not be code 1)
    std::string fname = "test_main_good.md";
    std::ofstream fout(fname, std::ios::binary);
    fout << "<details>\n<summary>\ntest\n</summary>\n</details>\n";
    fout.close();
    syntax_lint_p = fname;
    syntax_lint_errors.clear();
    check_md_file(fname);
    std::remove(fname.c_str());
    EXPECT_TRUE(syntax_lint_errors.empty());

    // BAD file (exit should be code 1 in Python; here just errors triggered)
    std::string fname2 = "test_main_bad.md";
    std::ofstream fot2(fname2, std::ios::binary);
    fot2 << "<details>\n";
    fot2.close();
    syntax_lint_p = fname2;
    syntax_lint_errors.clear();
    check_md_file(fname2);
    std::remove(fname2.c_str());
    EXPECT_TRUE(!syntax_lint_errors.empty());
}