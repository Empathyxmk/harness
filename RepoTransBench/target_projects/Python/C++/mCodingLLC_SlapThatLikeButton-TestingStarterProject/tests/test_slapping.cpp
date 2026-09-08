#include "slap_that_like_button.h"
#include <gtest/gtest.h>
#include <stdexcept>

TEST(TestSlapping, EmptySlap) {
    EXPECT_EQ(slap_many(LikeState::empty, ""), LikeState::empty);
}

TEST(TestSlapping, SingleSlaps) {
    EXPECT_EQ(slap_many(LikeState::empty, "l"), LikeState::liked);
    EXPECT_EQ(slap_many(LikeState::empty, "d"), LikeState::disliked);
}

struct MultiSlapParam { std::string input; LikeState expected; };

class MultiSlapsTest : public ::testing::TestWithParam<MultiSlapParam> {};
INSTANTIATE_TEST_SUITE_P(MultiSlapVariants, MultiSlapsTest, ::testing::Values(
    MultiSlapParam{"ll", LikeState::empty},
    MultiSlapParam{"dd", LikeState::empty},
    MultiSlapParam{"ld", LikeState::disliked},
    MultiSlapParam{"dl", LikeState::liked},
    MultiSlapParam{"ldd", LikeState::empty},
    MultiSlapParam{"lldd", LikeState::empty},
    MultiSlapParam{"ddl", LikeState::liked}
));
TEST_P(MultiSlapsTest, RunsCorrectly) {
    EXPECT_EQ(slap_many(LikeState::empty, GetParam().input), GetParam().expected);
}

// Skipped test: regexes not supported yet
// TEST(TestSlapping, RegexSlaps) {
//     EXPECT_EQ(slap_many(LikeState::empty, "[ld]*ddl"), LikeState::liked);
// }

// Known failing test (xfail)
TEST(TestSlapping, DISABLED_DivideByZero) {
    EXPECT_EQ(1 / 0, 1); // This will crash if enabled
}

TEST(TestSlapping, InvalidSlapThrows) {
    EXPECT_THROW(slap_many(LikeState::empty, "x"), std::invalid_argument);
}

// Xfail test with db (not implemented)
TEST(TestSlapping, DISABLED_DbSlap) {
    // No db support in this C++ translation
    // (Placeholders are not allowed, so we just disable the test)
}

#include <sstream>
#include <iostream>
TEST(TestSlapping, PrintOutput) {
    std::streambuf* orig_buf = std::cout.rdbuf();
    std::ostringstream capture;
    std::cout.rdbuf(capture.rdbuf());
    std::cout << "hello" << std::endl;
    std::cout.rdbuf(orig_buf);
    EXPECT_EQ(capture.str(), "hello\n");
}