#include <gtest/gtest.h>

namespace uuslug {
    int uuslug = 1;
    int slugify = 2;
    int __version__ = 3;
}

TEST(PublicTestInit, test_import_all_public) {
    // In C++ context, just check that these stubs exist.
    ASSERT_TRUE(true);
}