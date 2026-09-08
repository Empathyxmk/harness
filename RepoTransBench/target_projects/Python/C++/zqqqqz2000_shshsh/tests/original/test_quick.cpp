#include <gtest/gtest.h>

namespace shshsh {
namespace quick {
int square(int x) { return x * x; }
} // namespace quick
} // namespace shshsh

TEST(TestQuick, BasicSquare) {
    ASSERT_EQ(shshsh::quick::square(3), 9);
}