#include <gtest/gtest.h>

namespace hamms {
    inline int get_header() { return 1; }
}

TEST(PublicUtils, PublicTrue) {
    ASSERT_GT(10, 5);
}