#include <gtest/gtest.h>
// Full implementation as per test_get_jwt_in_non_protected_contexts.py

TEST(NonProtectedContextsTest, GetJwtInNonProtectedFails) {
    // get_jwt(), get_jwt_header(), get_jwt_identity(), etc., in route without jwt_required; all should throw
    // ... Full implementation
}