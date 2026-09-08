#include <gtest/gtest.h>
#include <string>
#include <vector>

struct Sushi {
    std::string fish;
    int pieces;
    Sushi(const std::string& fish_, int pieces_) : fish(fish_), pieces(pieces_) {}
};

// Edge property: at least one sushi type has >6 pieces
TEST(PublicSushiPropertyEdge, AtLeastOneSushiManyPiecesPublic) {
    std::vector<Sushi> sushis = {
        {"salmon", 8},
        {"tuna", 6}
    };
    bool found = false;
    for (const auto& sushi : sushis)
        if (sushi.pieces > 6)
            found = true;
    EXPECT_TRUE(found);
}