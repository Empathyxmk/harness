#include <gtest/gtest.h>
#include <string>
#include <vector>

struct Sushi {
    std::string fish;
    int pieces;
    Sushi(const std::string& fish_, int pieces_) : fish(fish_), pieces(pieces_) {}
};
static std::vector<Sushi> sushis = {
    {"salmon", 8},
    {"tuna", 6}
};

TEST(PublicSushiUnit, SushiFishNamePublic) {
    for (const auto& sushi : sushis)
        EXPECT_FALSE(sushi.fish.empty());
}

TEST(PublicSushiUnit, SushiPiecesPositivePublic) {
    for (const auto& sushi : sushis)
        EXPECT_GT(sushi.pieces, 0);
}