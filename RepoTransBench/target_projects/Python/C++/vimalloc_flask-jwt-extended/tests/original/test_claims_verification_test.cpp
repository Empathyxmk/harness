#include <gtest/gtest.h>
// Full implementation as per test_claims_verification.py

TEST(ClaimsVerificationTest, SuccessfulValidation) {
    // token_verification_loader returns True, test different endpoints
    // ... Full implementation
}

TEST(ClaimsVerificationTest, UnsuccessfulValidation) {
    // token_verification_loader returns False, check error
    // ... Full implementation
}

TEST(ClaimsVerificationTest, ClaimsValidationCustomError) {
    // Custom token_verification_failed_loader, check error message and code
    // ... Full implementation
}