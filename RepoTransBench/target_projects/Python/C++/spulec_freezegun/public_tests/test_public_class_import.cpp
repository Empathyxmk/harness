#include <gtest/gtest.h>
#include <cmath>

TEST(PublicClassImportTest, ImportClassDifferentName) {
    ASSERT_DOUBLE_EQ(std::sqrt(81), 9.0);
}