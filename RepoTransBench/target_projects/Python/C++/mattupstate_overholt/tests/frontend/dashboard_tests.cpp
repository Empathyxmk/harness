#include <gtest/gtest.h>
#include "tests/frontend/overholt_frontend_test_case.h"

class DashboardTestCase : public OverholtFrontendTestCase {
};

TEST_F(DashboardTestCase, AuthenticatedDashboardAccess) {
    FrontendResponse r = get("/");
    ASSERT_TRUE(assertOk(r));
    ASSERT_NE(r.data.find("<h1>Dashboard</h1>"), std::string::npos);
}

TEST_F(DashboardTestCase, UnauthenticatedDashboardAccess) {
    get("/logout");
    FrontendResponse r = get("/");
    ASSERT_TRUE(assertOk(r));
    ASSERT_EQ(r.data.find("<h1>Dashboard</h1>"), std::string::npos);
}