#include <gtest/gtest.h>
#include <stdexcept>
#include <string>

// Simulated mockup for testing interface
class CoqtopPy {
public:
    std::string version() const { return "8.13.2"; }
    bool check_syntax(const std::string& code) {
        if (code.empty())
            throw std::runtime_error("No code provided");
        return code.find("SyntaxErr") == std::string::npos;
    }
};

class CoqtopPyTest : public ::testing::Test {
protected:
    CoqtopPy coqtop;
};

TEST_F(CoqtopPyTest, Version_IsCorrect) {
    EXPECT_EQ(coqtop.version(), "8.13.2");
}

TEST_F(CoqtopPyTest, CheckSyntax_CorrectCode) {
    EXPECT_TRUE(coqtop.check_syntax("Lemma test: True. Proof. exact I. Qed."));
}

TEST_F(CoqtopPyTest, CheckSyntax_SyntaxError) {
    EXPECT_FALSE(coqtop.check_syntax("Lemma SyntaxErr: True"));
}

TEST_F(CoqtopPyTest, CheckSyntax_EmptyCodeThrows) {
    EXPECT_THROW(coqtop.check_syntax(""), std::runtime_error);
}