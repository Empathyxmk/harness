#include "slap_that_like_button.h"
#include <gtest/gtest.h>
#include <stdexcept>

struct PublicSlapLikeParam { LikeState initial; LikeState expected; };
class PublicSlapLikeTest : public ::testing::TestWithParam<PublicSlapLikeParam> {};
INSTANTIATE_TEST_SUITE_P(PublicSlapLikeCases, PublicSlapLikeTest, ::testing::Values(
    PublicSlapLikeParam{LikeState::empty, LikeState::liked},
    PublicSlapLikeParam{LikeState::liked, LikeState::empty},
    PublicSlapLikeParam{LikeState::disliked, LikeState::liked}
));
TEST_P(PublicSlapLikeTest, Works) {
    EXPECT_EQ(slap(GetParam().initial, "l"), GetParam().expected);
}

struct PublicSlapDislikeParam { LikeState initial; LikeState expected; };
class PublicSlapDislikeTest : public ::testing::TestWithParam<PublicSlapDislikeParam> {};
INSTANTIATE_TEST_SUITE_P(PublicSlapDislikeCases, PublicSlapDislikeTest, ::testing::Values(
    PublicSlapDislikeParam{LikeState::empty, LikeState::disliked},
    PublicSlapDislikeParam{LikeState::liked, LikeState::disliked},
    PublicSlapDislikeParam{LikeState::disliked, LikeState::empty}
));
TEST_P(PublicSlapDislikeTest, Works) {
    EXPECT_EQ(slap(GetParam().initial, "d"), GetParam().expected);
}

TEST(TestPublicSlap, InvalidActionThrows) {
    EXPECT_THROW(slap(LikeState::empty, "x"), std::invalid_argument);
}

TEST(TestPublicSlap, ManyLikeStreak) {
    EXPECT_EQ(slap_many(LikeState::liked, "ll"), LikeState::liked);
}
TEST(TestPublicSlap, ManyDislikeStreak) {
    EXPECT_EQ(slap_many(LikeState::disliked, "d"), LikeState::empty);
    EXPECT_EQ(slap_many(LikeState::empty, "dd"), LikeState::empty);
}

struct PublicStatesNewParam { LikeState initial; std::string seq; LikeState final_s; };
class PublicStatesNewTest : public ::testing::TestWithParam<PublicStatesNewParam> {};
INSTANTIATE_TEST_SUITE_P(PublicStatesNewCases, PublicStatesNewTest, ::testing::Values(
    PublicStatesNewParam{LikeState::empty, "dll", LikeState::liked},
    PublicStatesNewParam{LikeState::liked, "dl", LikeState::disliked},
    PublicStatesNewParam{LikeState::liked, "dld", LikeState::empty}
));
TEST_P(PublicStatesNewTest, Works) {
    EXPECT_EQ(slap_many(GetParam().initial, GetParam().seq), GetParam().final_s);
}

struct PublicStatesSimpleParam { LikeState initial; std::string seq; LikeState final_s; };
class PublicStatesSimpleTest : public ::testing::TestWithParam<PublicStatesSimpleParam> {};
INSTANTIATE_TEST_SUITE_P(PublicStatesSimpleCases, PublicStatesSimpleTest, ::testing::Values(
    PublicStatesSimpleParam{LikeState::empty, "", LikeState::empty},
    PublicStatesSimpleParam{LikeState::empty, "l", LikeState::liked},
    PublicStatesSimpleParam{LikeState::liked, "d", LikeState::disliked},
    PublicStatesSimpleParam{LikeState::disliked, "l", LikeState::liked}
));
TEST_P(PublicStatesSimpleTest, Works) {
    EXPECT_EQ(slap_many(GetParam().initial, GetParam().seq), GetParam().final_s);
}

struct PublicAutoSlapLikesParam { int presses; LikeState expected; };
class PublicAutoSlapLikesTest : public ::testing::TestWithParam<PublicAutoSlapLikesParam> {};
INSTANTIATE_TEST_SUITE_P(PublicAutoSlapLikesCases, PublicAutoSlapLikesTest, ::testing::Values(
    PublicAutoSlapLikesParam{1, LikeState::liked},
    PublicAutoSlapLikesParam{2, LikeState::empty},
    PublicAutoSlapLikesParam{3, LikeState::liked},
    PublicAutoSlapLikesParam{6, LikeState::empty}
));
TEST_P(PublicAutoSlapLikesTest, Likes) {
    EXPECT_EQ(auto_slap(GetParam().presses, "like"), GetParam().expected);
}

struct PublicAutoSlapDislikesParam { int presses; LikeState expected; };
class PublicAutoSlapDislikesTest : public ::testing::TestWithParam<PublicAutoSlapDislikesParam> {};
INSTANTIATE_TEST_SUITE_P(PublicAutoSlapDislikesCases, PublicAutoSlapDislikesTest, ::testing::Values(
    PublicAutoSlapDislikesParam{1, LikeState::disliked},
    PublicAutoSlapDislikesParam{2, LikeState::empty},
    PublicAutoSlapDislikesParam{3, LikeState::disliked},
    PublicAutoSlapDislikesParam{6, LikeState::empty}
));
TEST_P(PublicAutoSlapDislikesTest, Dislikes) {
    EXPECT_EQ(auto_slap(GetParam().presses, "dislike"), GetParam().expected);
}

class PublicAutoSlapInvalidTest : public ::testing::TestWithParam<std::string> {};
INSTANTIATE_TEST_SUITE_P(PublicAutoSlapInvalidCases, PublicAutoSlapInvalidTest, ::testing::Values(
    "foo", "", "NULL"
));
TEST_P(PublicAutoSlapInvalidTest, Throws) {
    // For "NULL" in C++ test, it's not the same as None, but covers invalid anyway
    EXPECT_THROW(auto_slap(1, GetParam()), std::invalid_argument);
}