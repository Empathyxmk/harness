#include <gtest/gtest.h>
#include <string>
#include "claude_to_chatgpt/logger.h"

TEST(PublicLoggerTest, PublicGetLoggerLevel) {
    Logger logger = get_logger("publicLoggerTest");
    EXPECT_TRUE(logger.is_valid());
    logger.set_level(Logger::Level::ERROR);
    EXPECT_EQ(logger.get_level(), Logger::Level::ERROR);
}

TEST(PublicLoggerTest, PublicGetLoggerName) {
    std::string logger_name = "unique_logger_name";
    Logger logger = get_logger(logger_name);
    EXPECT_EQ(logger.get_name(), logger_name);
}