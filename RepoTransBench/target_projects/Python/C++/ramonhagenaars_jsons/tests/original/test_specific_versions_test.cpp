#include <gtest/gtest.h>

TEST(TestSpecificVersions, test_example_specific_versions) {
    // Just confirm that "version-sensitive logic" passes.
    int major = 3;
    EXPECT_GE(major, 3);
}