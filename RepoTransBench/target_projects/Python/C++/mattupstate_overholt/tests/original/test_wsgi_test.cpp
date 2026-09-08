#include <gtest/gtest.h>
#include "wsgi.h"

TEST(WSGITest, WSGIApplicationExists) {
    // Application should exist in wsgi
    EXPECT_TRUE(wsgi::has_application());
}

TEST(WSGITest, WSGIMainRunSimpleCanBePatched) {
    // Test logic for patching run_simple - we can only simulate here
    bool called = false;
    auto fake_run_simple = [&](const std::string&, int, void*, bool, bool) {
        called = true;
        return std::string("ran");
    };
    wsgi::set_run_simple(fake_run_simple);
    wsgi::reload_module(); // Simulate reload/entry
    EXPECT_TRUE(wsgi::has_application());
    EXPECT_TRUE(called);
}