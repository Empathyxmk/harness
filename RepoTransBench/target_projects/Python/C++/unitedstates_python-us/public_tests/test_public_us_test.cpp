#include <gtest/gtest.h>
#include "us.h"

using namespace us;

TEST(PublicUsTest, FipsLookup) {
    EXPECT_EQ(lookup("48"), &TX);
}

TEST(PublicUsTest, AbbrLookup) {
    EXPECT_EQ(lookup("CO"), nullptr); // CO not in our test STATES, so expect nullptr
}

TEST(PublicUsTest, NameLookup) {
    EXPECT_EQ(lookup("Florida"), &FL);
}

TEST(PublicUsTest, MetaphoneLookup) {
    EXPECT_EQ(lookup("Minissota"), &MN);
}

TEST(PublicUsTest, MetaphoneLookupCaps) {
    EXPECT_EQ(lookup("ILLINOYS"), &IL);
}

TEST(PublicUsTest, LookupWithIntegerInput) {
    EXPECT_EQ(lookup("12"), &FL);
}

TEST(PublicUsTest, LookupWithField) {
    EXPECT_EQ(lookup("Madison", "capital"), &WI);
}

TEST(PublicUsTest, NonExistantLookupReturnsNone) {
    EXPECT_EQ(lookup("GOTHAMCITY"), nullptr);
}

TEST(PublicUsTest, TerritoryLookup) {
    EXPECT_EQ(lookup("PR"), &PR);
}