#include "slap_that_like_button.h"
#include <gtest/gtest.h>

TEST(TestPublicSlapping, AlternateLikesDislikes) {
    EXPECT_EQ(slap_many(LikeState::empty, "ldld"), LikeState::liked);
    EXPECT_EQ(slap_many(LikeState::liked, "dldl"), LikeState::liked);
}

TEST(TestPublicSlapping, FullCycle) {
    EXPECT_EQ(slap_many(LikeState::liked, "ldl"), LikeState::disliked);
}

TEST(TestPublicSlapping, InvalidCharSequence) {
    EXPECT_THROW(slap_many(LikeState::empty, "zqyz"), std::invalid_argument);
}

struct PublicAutoSlapCyclesParam { int num; std::string action; LikeState final_s; };
class PublicAutoSlapCyclesTest : public ::testing::TestWithParam<PublicAutoSlapCyclesParam> {};
INSTANTIATE_TEST_SUITE_P(PublicAutoSlapCyclesCases, PublicAutoSlapCyclesTest, ::testing::Values(
    PublicAutoSlapCyclesParam{4, "like", LikeState::empty},
    PublicAutoSlapCyclesParam{5, "like", LikeState::liked},
    PublicAutoSlapCyclesParam{7, "dislike", LikeState::disliked},
    PublicAutoSlapCyclesParam{0, "dislike", LikeState::empty}
));
TEST_P(PublicAutoSlapCyclesTest, Cycles) {
    EXPECT_EQ(auto_slap(GetParam().num, GetParam().action), GetParam().final_s);
}

TEST(TestPublicSlapping, AutoSlapInvalidNum) {
    // throws because the first argument is a string but function expects int
    // simulate this: can't compile with wrong type, so test invalid negative integer instead
    EXPECT_THROW(auto_slap(-1, "like"), std::invalid_argument);
}