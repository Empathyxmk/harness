#include <gtest/gtest.h>
#include "underscore.h"
#include <string>

using namespace underscore;

TEST(TestPublicBasics, IdentityPublic) {
    EXPECT_EQ(identity(std::string("underscore")), "underscore");
}