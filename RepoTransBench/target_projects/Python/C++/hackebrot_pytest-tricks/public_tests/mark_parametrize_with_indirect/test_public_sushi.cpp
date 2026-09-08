#include <gtest/gtest.h>
#include <vector>
#include <string>

// Indirect parameterization test
struct Sushi {
    std::string fish;
    int pieces;
    Sushi(const std::string& fish_, int pieces_) : fish(fish_), pieces(pieces_) {}
};

std::vector<Sushi> sushi_data() {
    return { Sushi("salmon", 8), Sushi("tuna", 6) };
}

TEST(PublicSushi, FishNameNotEmptyPublic) {
    for (const auto& sushi : sushi_data())
        EXPECT_FALSE(sushi.fish.empty());
}

TEST(PublicSushi, PiecesArePositivePublic) {
    for (const auto& sushi : sushi_data())
        EXPECT_GT(sushi.pieces, 0);
}