#include <gtest/gtest.h>
#include "greedypacker/guillotine.h"
#include "greedypacker/item.h"

class TestPublicGuillotine : public ::testing::Test {
protected:
    void SetUp() override {
        G = new greedypacker::Guillotine(14, 13, "short_side");
    }
    void TearDown() override {
        delete G;
    }
    greedypacker::Guillotine* G;
};

TEST_F(TestPublicGuillotine, InsertAndCoordinates) {
    greedypacker::Item I(8, 4);
    bool result = G->insert(I);
    EXPECT_TRUE(result);
    EXPECT_GE(G->width, I.x + I.width);
    EXPECT_GE(G->height, I.y + I.height);
}

TEST_F(TestPublicGuillotine, InvalidHeuristic) {
    EXPECT_THROW(greedypacker::Guillotine(4, 7, "nonsense"), std::invalid_argument);
}