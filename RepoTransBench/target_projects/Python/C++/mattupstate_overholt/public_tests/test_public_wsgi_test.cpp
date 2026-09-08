#include <gtest/gtest.h>
#include "wsgi.h"
#include "werkzeug/dispatcher_middleware.h"

// Test that application is a DispatcherMiddleware
TEST(PublicWSGITest, ApplicationType) {
    EXPECT_TRUE(dynamic_cast<werkzeug::DispatcherMiddleware*>(wsgi::application) != nullptr);
}

TEST(PublicWSGITest, ApplicationMounts) {
    auto dispatcher = dynamic_cast<werkzeug::DispatcherMiddleware*>(wsgi::application);
    ASSERT_TRUE(dispatcher != nullptr);
    EXPECT_TRUE(dispatcher->mounts.count("/api") > 0);
}