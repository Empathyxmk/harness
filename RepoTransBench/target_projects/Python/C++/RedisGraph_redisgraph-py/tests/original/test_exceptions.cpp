#include <gtest/gtest.h>
#include "exceptions.h"

using namespace redisgraph;

TEST(TestExceptions, VersionMismatchException) {
    std::string ver = "2.10.0";
    VersionMismatchException e(ver);
    EXPECT_TRUE(dynamic_cast<VersionMismatchException*>(&e) != nullptr);
    EXPECT_EQ(e.version, ver);
}