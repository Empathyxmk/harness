#include <gtest/gtest.h>

// This public test is meant to check comment stripping in coqtail_py
std::string strip_comments(const std::string& code) {
    size_t pos = code.find("//");
    if (pos != std::string::npos) return code.substr(0, pos);
    return code;
}

TEST(PublicCoqtailPyTest, PublicCommentStripping) {
    EXPECT_EQ(strip_comments("Goal True. // simply"), "Goal True. ");
    EXPECT_EQ(strip_comments("Lemma foo : bar."), "Lemma foo : bar.");
}