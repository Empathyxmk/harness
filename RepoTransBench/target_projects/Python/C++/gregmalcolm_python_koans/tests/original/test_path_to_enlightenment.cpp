#include "gtest/gtest.h"
#include "lib/path_to_enlightenment.h"
#include <sstream>
#include <vector>
#include <string>

// Helper to easily capture multi-line string input
static std::istringstream make_stream(const std::vector<std::string>& lines) {
    std::ostringstream oss;
    for (size_t i = 0; i < lines.size(); ++i)
        oss << lines[i] << (i+1 == lines.size() ? "" : "\n");
    return std::istringstream(oss.str());
}

TEST(TestFilterKoanNames, EmptyInputProducesEmptyOutput) {
    std::istringstream infile("");
    std::vector<std::string> expected;
    std::vector<std::string> received = filter_koan_names(infile);
    EXPECT_EQ(expected, received);
}

TEST(TestFilterKoanNames, NamesYieldedMatchNamesInFile) {
    std::vector<std::string> names = {
        "this.is.a.test",
        "this.is.only.a.test"
    };
    std::istringstream infile = make_stream(names);
    std::vector<std::string> received = filter_koan_names(infile);
    EXPECT_EQ(names, received);
}

TEST(TestFilterKoanNames, WhitespaceIsStripped) {
    std::vector<std::string> names = {
        "this.is.a.test",
        "    white.space.should.be.stripped",
        "this.is.only.a.test",
        "white.space.should.be.stripped    "
    };
    std::istringstream infile = make_stream(names);
    std::vector<std::string> expected = {
        "this.is.a.test",
        "white.space.should.be.stripped",
        "this.is.only.a.test",
        "white.space.should.be.stripped"
    };
    std::vector<std::string> received = filter_koan_names(infile);
    EXPECT_EQ(expected, received);
}

TEST(TestFilterKoanNames, CommentedOutNamesAreExcluded) {
    std::vector<std::string> names = {
        "this.is.a.test",
        "#this.is.a.comment",
        "this.is.only.a.test",
        "    #    this.is.also a.comment    "
    };
    std::istringstream infile = make_stream(names);
    std::vector<std::string> expected = {
        "this.is.a.test",
        "this.is.only.a.test"
    };
    std::vector<std::string> received = filter_koan_names(infile);
    EXPECT_EQ(expected, received);
}

TEST(TestFilterKoanNames, AllBlankOrCommentLinesProduceEmptyOutput) {
    std::vector<std::string> names = {
        " ",
        "# This is a comment.",
        "\t",
        "    # This is also a comment."
    };
    std::istringstream infile = make_stream(names);
    std::vector<std::string> expected;
    std::vector<std::string> received = filter_koan_names(infile);
    EXPECT_EQ(expected, received);
}

// Suite tests
#include "lib/koans_suite.h"  // define koans_suite and its adjunct logic

TEST(TestKoansSuite, EmptyInputProducesEmptyTestSuite) {
    std::vector<std::string> names;
    auto suite = koans_suite(names);
    // Return type must be a TestSuite; receive must be empty
    ASSERT_TRUE(isTestSuite(suite));
    EXPECT_TRUE(suite.tests().empty());
}

TEST(TestKoansSuite, TestcaseNamesAppearInTestSuite) {
    std::vector<std::string> names = {
        "koans.about_asserts.AboutAsserts",
        "koans.about_none.AboutNone",
        "koans.about_strings.AboutStrings"
    };
    auto suite = koans_suite(names);
    std::vector<std::string> expected = {
        "AboutAsserts",
        "AboutNone",
        "AboutStrings"
    };
    std::set<std::string> received_names;
    for (const auto& test : suite.tests()) {
        received_names.insert(test->class_name());
    }
    std::vector<std::string> received(received_names.begin(), received_names.end());
    std::sort(expected.begin(), expected.end());
    std::sort(received.begin(), received.end());
    EXPECT_EQ(expected, received);
}