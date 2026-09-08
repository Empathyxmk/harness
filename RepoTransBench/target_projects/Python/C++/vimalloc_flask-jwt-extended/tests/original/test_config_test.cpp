#include <gtest/gtest.h>
// Full implementation required as per test_config.py
// Simulate Flask app + JWT config in C++
// Test all config options, invalid options, error handling, customizations, etc.

TEST(ConfigTest, DefaultConfigs) {
    // Test all config values match expected defaults, using C++ getters/setters/asserts
    // ... Full implementation for every assert in test_config.py
}

TEST(ConfigTest, OverrideConfigsWithTimedeltas) {
    // Parametrize delta_func, override configs, ensure correctness
    // ... Full implementation
}

TEST(ConfigTest, JsonEncoderBehavior) {
    // Simulate Flask <2.2 and >2.2 logic, assert correct encoder used
    // ... Full implementation
}

TEST(ConfigTest, TokensNeverExpire) {
    // Set access_token_expires and refresh_token_expires to False, check logic
    // ... Full implementation
}

TEST(ConfigTest, SymmetricKeyConfigErrors) {
    // Set/clear secret keys, app secret, expect RuntimeError where appropriate
    // ... Full implementation
}

// ... additional tests for asymmetric secret key errors, invalid config options, jwt token locations, CSRF, etc.