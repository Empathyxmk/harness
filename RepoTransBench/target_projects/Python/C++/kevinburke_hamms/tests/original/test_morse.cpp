#include <gtest/gtest.h>

namespace hamms {
    namespace morse {
        inline int dummy() { return 1; }
    }
}

TEST(Morse, Dummy) {
    ASSERT_TRUE(true);
}