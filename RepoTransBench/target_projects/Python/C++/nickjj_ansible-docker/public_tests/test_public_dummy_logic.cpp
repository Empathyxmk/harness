#include <gtest/gtest.h>
#include "dummy_logic.h"

TEST(PublicDummyLogic, IncrementPublic) {
    EXPECT_EQ(dummy_logic::increment(10), 11);
    EXPECT_EQ(dummy_logic::increment(-4), -3);
}

TEST(PublicDummyLogic, SumPublic) {
    EXPECT_EQ(dummy_logic::total({3, 8, 12}), 23);
    EXPECT_EQ(dummy_logic::total({}), 0);
    EXPECT_EQ(dummy_logic::total({-2, 5}), 3);
}

TEST(PublicDummyLogic, IsEvenPublic) {
    EXPECT_TRUE(dummy_logic::is_even(100));
    EXPECT_FALSE(dummy_logic::is_even(15));
    EXPECT_TRUE(dummy_logic::is_even(-22));
}

TEST(PublicDummyLogic, CustomCasePublic) {
    std::vector<int> numbers = {6, 7, 8, 9};
    int even_count = 0;
    for (int n: numbers) if (dummy_logic::is_even(n)) ++even_count;
    EXPECT_EQ(even_count, 2);
}

TEST(PublicDummyLogic, ZeroIncrementPublic) {
    EXPECT_EQ(dummy_logic::increment(0), 1);
}

TEST(PublicDummyLogic, NegativeTotalPublic) {
    EXPECT_EQ(dummy_logic::total({-5, -5, -10}), -20);
}