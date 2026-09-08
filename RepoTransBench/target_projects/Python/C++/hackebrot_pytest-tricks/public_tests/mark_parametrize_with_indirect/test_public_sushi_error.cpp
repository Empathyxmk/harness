#include <gtest/gtest.h>
#include <stdexcept>
#include <string>

struct Sushi {
    std::string fish;
    int pieces;
    Sushi(const std::string& fish_, int pieces_) : fish(fish_), pieces(pieces_) {}
};

void make_sushi(const std::string& fish, int pieces) {
    if (fish.empty() || pieces <= 0)
        throw std::invalid_argument("Invalid sushi parameters");
}

TEST(PublicSushiError, ThrowOnInvalidFishPublic) {
    EXPECT_THROW(make_sushi("", 5), std::invalid_argument);
}

TEST(PublicSushiError, ThrowOnNonPositivePiecesPublic) {
    EXPECT_THROW(make_sushi("salmon", 0), std::invalid_argument);
    EXPECT_THROW(make_sushi("tuna", -1), std::invalid_argument);
}