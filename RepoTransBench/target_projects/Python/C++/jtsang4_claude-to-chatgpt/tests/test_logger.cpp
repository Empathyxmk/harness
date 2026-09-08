#include <gtest/gtest.h>
#include "claude_to_chatgpt/logger.h"

TEST(LoggerTest, LoggerImportable) {
    Logger logger = get_logger();
    // Should return correct Logger type
    EXPECT_TRUE(logger.is_valid());
}