#include <gtest/gtest.h>
#include <string>
#include <map>

struct Sushi {
    std::string fish;
    int pieces;
    Sushi(const std::string& fish_, int pieces_) : fish(fish_), pieces(pieces_) {}
};

Sushi sushi_fixture(const std::string& fish = "salmon", int pieces = 8) {
    return Sushi(fish, pieces);
}

TEST(PublicConftestIntegration, DefaultSushiFixturePublic) {
    Sushi s = sushi_fixture();
    EXPECT_EQ(s.fish, "salmon");
    EXPECT_EQ(s.pieces, 8);
}

TEST(PublicConftestIntegration, CustomSushiFixturePublic) {
    Sushi s = sushi_fixture("tuna", 10);
    EXPECT_EQ(s.fish, "tuna");
    EXPECT_EQ(s.pieces, 10);
}