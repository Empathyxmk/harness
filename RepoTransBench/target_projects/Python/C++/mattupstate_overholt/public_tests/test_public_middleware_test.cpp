#include <gtest/gtest.h>
#include "overholt/middleware.h"

TEST(PublicMiddlewareTest, MiddlewareModuleExists) {
    // Check that the middleware module (namespace/class) defines a doc attribute (simulate __doc__ in Python)
    EXPECT_TRUE(Overholt::middleware_doc() != nullptr);
}