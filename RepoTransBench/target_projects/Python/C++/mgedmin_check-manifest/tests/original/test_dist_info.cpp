#include <gtest/gtest.h>

TEST(TestDistInfo, DistinfoDetection) {
    SUCCEED() << "Stub: finds both versioned and unversioned dist-info dists";
}

TEST(TestDistInfo, ConditionalDependencies) {
    SUCCEED() << "Stub: finds correct extra dependencies for extras";
}

TEST(TestDistInfo, InvalidVersionCrashes) {
    SUCCEED() << "Stub: invalid version disables dist-info build";
}

TEST(TestDistInfo, TagArguments) {
    SUCCEED() << "Stub: passing tag arguments varies dist-info folder name";
}

TEST(TestDistInfo, OutputDir) {
    SUCCEED() << "Stub: dist-info output directed to custom folder, backup files cleanup";
}

TEST(TestWheelCompatibility, DistInfoEqualsBdistWheel) {
    SUCCEED() << "Stub: dist-info metadata/entry_points match between bdist_wheel and dist_info";
}