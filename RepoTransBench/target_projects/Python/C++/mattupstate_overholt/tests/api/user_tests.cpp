#include <gtest/gtest.h>
#include "tests/api/overholt_api_test_case.h"

class UserApiTestCase : public OverholtApiTestCase {
    // Provide fixtures if needed
};

TEST_F(UserApiTestCase, GetCurrentUser) {
    ApiResponse r = jget("/users");
    ASSERT_TRUE(assertOkJson(r));
}

TEST_F(UserApiTestCase, GetUser) {
    ApiResponse r = jget("/users/" + std::to_string(user.id));
    ASSERT_TRUE(assertOkJson(r));
}