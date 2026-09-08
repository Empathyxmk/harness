#include <gtest/gtest.h>

// Mockup of CoqtailPy logic for unit testing
// In practice, you would implement the actual C++ logic; here we use an example to demonstrate test translation.

std::string strip_comments(const std::string& input) {
    size_t pos = input.find("//");
    if (pos != std::string::npos)
        return input.substr(0, pos);
    return input;
}

class CoqtailPyTest : public ::testing::Test {};

TEST_F(CoqtailPyTest, StripComments_RemovesSingleLineComments) {
    std::string code = "Check nat. // comment";
    std::string expected = "Check nat. ";
    EXPECT_EQ(strip_comments(code), expected);
}

TEST_F(CoqtailPyTest, StripComments_LeavesNoCommentLinesUnchanged) {
    std::string code = "Lemma test : True.";
    std::string expected = "Lemma test : True.";
    EXPECT_EQ(strip_comments(code), expected);
}

TEST_F(CoqtailPyTest, StripComments_EmptyString) {
    std::string code = "";
    std::string expected = "";
    EXPECT_EQ(strip_comments(code), expected);
}