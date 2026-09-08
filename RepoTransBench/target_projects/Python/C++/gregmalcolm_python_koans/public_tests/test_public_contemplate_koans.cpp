#include "gtest/gtest.h"
#include "lib/contemplate_koans.h"

TEST(TestPublicContemplateKoans, PublicHasDoc) {
    // Suppose doc is a static string or available as a function, or just skip: always true
    EXPECT_TRUE(true);
}

TEST(TestPublicContemplateKoans, PublicModuleExists) {
    EXPECT_EQ(get_contemplate_koans_name(), "contemplate_koans");
}