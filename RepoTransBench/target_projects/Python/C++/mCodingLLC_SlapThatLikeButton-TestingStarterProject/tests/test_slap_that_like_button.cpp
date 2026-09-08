#include "slap_that_like_button.h"
#include <gtest/gtest.h>

// Test LikeState transitions for slap_like
TEST(TestSlapThatLikeButton, SlapLikeTransitions) {
    EXPECT_EQ(slap_like(LikeState::empty), LikeState::liked);
    EXPECT_EQ(slap_like(LikeState::liked), LikeState::empty);
    EXPECT_EQ(slap_like(LikeState::disliked), LikeState::liked);
}

TEST(TestSlapThatLikeButton, SlapDislikeTransitions) {
    EXPECT_EQ(slap_dislike(LikeState::empty), LikeState::disliked);
    EXPECT_EQ(slap_dislike(LikeState::liked), LikeState::disliked);
    EXPECT_EQ(slap_dislike(LikeState::disliked), LikeState::empty);
}

struct SlapManyParams {
    LikeState initial;
    std::string slap_seq;
    LikeState final_expected;
};

// Parameterized-style test for slap_many
class SlapManyStatesTest : public ::testing::TestWithParam<SlapManyParams> {};

INSTANTIATE_TEST_SUITE_P(
    SlapManyStatesVariants,
    SlapManyStatesTest,
    ::testing::Values(
        SlapManyParams{LikeState::liked, "", LikeState::liked},
        SlapManyParams{LikeState::disliked, "", LikeState::disliked},
        SlapManyParams{LikeState::liked, "l", LikeState::empty},
        SlapManyParams{LikeState::liked, "d", LikeState::disliked},
        SlapManyParams{LikeState::liked, "ld", LikeState::disliked},
        SlapManyParams{LikeState::disliked, "l", LikeState::liked},
        SlapManyParams{LikeState::disliked, "d", LikeState::empty},
        SlapManyParams{LikeState::liked, "dl", LikeState::liked}
    )
);

TEST_P(SlapManyStatesTest, OtherStatesSlapMany) {
    const auto& p = GetParam();
    EXPECT_EQ(slap_many(p.initial, p.slap_seq), p.final_expected);
}

TEST(TestSlapThatLikeButton, SlapManyUpperCase) {
    EXPECT_EQ(slap_many(LikeState::empty, "L"), LikeState::liked);
    EXPECT_EQ(slap_many(LikeState::liked, "D"), LikeState::disliked);
    EXPECT_EQ(slap_many(LikeState::disliked, "L"), LikeState::liked);
    // Mixed
    EXPECT_EQ(slap_many(LikeState::empty, "lD"), LikeState::disliked);
    EXPECT_EQ(slap_many(LikeState::liked, "Dl"), LikeState::liked);
}

class BadSlapManyTest : public ::testing::TestWithParam<std::string> {};
INSTANTIATE_TEST_SUITE_P(BadSlapManyCases, BadSlapManyTest, ::testing::Values(
    "x", "z", " ", "1", "-", "_", "LdX"
));

TEST_P(BadSlapManyTest, ThrowsOnInvalidInput) {
    EXPECT_THROW(slap_many(LikeState::empty, GetParam()), std::invalid_argument);
}