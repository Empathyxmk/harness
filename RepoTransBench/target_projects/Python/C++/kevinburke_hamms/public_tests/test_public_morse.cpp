#include <gtest/gtest.h>
#include <typeinfo>

namespace hamms {
    namespace morse { int dummy() { return 1; } }
}

TEST(PublicMorse, MorseIsObject) {
    ASSERT_TRUE(typeid(hamms::morse) == typeid(hamms::morse));
}