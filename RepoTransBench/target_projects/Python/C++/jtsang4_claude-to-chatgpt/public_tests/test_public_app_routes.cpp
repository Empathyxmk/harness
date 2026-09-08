#include <gtest/gtest.h>
#include <string>
#include "claude_to_chatgpt/app.h"

TEST(PublicAppRoutes, PublicHealthRoute) {
    auto resp = app_get_healthz();
    EXPECT_EQ(resp.status_code, 200);
    EXPECT_TRUE(resp.body == "\"ok\"" || resp.body == "ok" || resp.body == "'ok'");
}

TEST(PublicAppRoutes, PublicNotFoundRoute) {
    auto resp = app_get("/non-existent-endpoint2123");
    EXPECT_EQ(resp.status_code, 404);
}

TEST(PublicAppRoutes, PublicRootRoute) {
    auto resp = app_get("/");
    EXPECT_TRUE(resp.status_code == 404 || resp.status_code == 200);
    // Body robustness not asserted.
}

TEST(PublicAppRoutes, PublicOptionsReturns405OrOk) {
    auto resp = app_options("/healthz");
    EXPECT_TRUE(resp.status_code == 405 || resp.status_code == 200 || resp.status_code == 204);
}