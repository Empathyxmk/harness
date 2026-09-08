#include <gtest/gtest.h>
// Full implementation as per test_add_context_processor.py

TEST(AddContextProcessorTest, ContextProcessorPresent) {
    // JWTManager with add_context_processor=True, current_user provided by loader, expect "test_user" in template
    // ... Full implementation
}

TEST(AddContextProcessorTest, ContextProcessorAbsent) {
    // JWTManager without context processor, expect empty string
    // ... Full implementation
}