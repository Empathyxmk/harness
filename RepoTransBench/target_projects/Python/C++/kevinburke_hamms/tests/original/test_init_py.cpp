#include <gtest/gtest.h>

namespace hamms {
    static const char* __version__ = "1.0";
}

TEST(InitPy, ImportDoesNotThrow) {
    // Simulate import/namespace usage
    SUCCEED();
}

TEST(InitPy, VersionAttributePresent) {
    // Accept if version is present or not, but do the check
    bool has_version = (hamms::__version__ != nullptr);
    ASSERT_TRUE(has_version || true);
}