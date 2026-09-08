#include <gtest/gtest.h>
#include "pynubank/parsing.h"

TEST(PublicParsingTest, ParsesCorrectly) {
    Parsing parser;
    auto obj = parser.parse("{\"x\": 42}");
    EXPECT_EQ(obj["x"], 42);
}