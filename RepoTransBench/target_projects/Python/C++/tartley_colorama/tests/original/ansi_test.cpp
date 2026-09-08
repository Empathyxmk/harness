#include <gtest/gtest.h>
#include "colorama/ansi.h"

using namespace colorama;

TEST(AnsiTest, ForeAttributes) {
    EXPECT_STREQ(Fore::BLACK, "\033[30m");
    EXPECT_STREQ(Fore::RED, "\033[31m");
    EXPECT_STREQ(Fore::GREEN, "\033[32m");
    EXPECT_STREQ(Fore::YELLOW, "\033[33m");
    EXPECT_STREQ(Fore::BLUE, "\033[34m");
    EXPECT_STREQ(Fore::MAGENTA, "\033[35m");
    EXPECT_STREQ(Fore::CYAN, "\033[36m");
    EXPECT_STREQ(Fore::WHITE, "\033[37m");
    EXPECT_STREQ(Fore::RESET, "\033[39m");
    EXPECT_STREQ(Fore::LIGHTBLACK_EX, "\033[90m");
    EXPECT_STREQ(Fore::LIGHTRED_EX, "\033[91m");
    EXPECT_STREQ(Fore::LIGHTGREEN_EX, "\033[92m");
    EXPECT_STREQ(Fore::LIGHTYELLOW_EX, "\033[93m");
    EXPECT_STREQ(Fore::LIGHTBLUE_EX, "\033[94m");
    EXPECT_STREQ(Fore::LIGHTMAGENTA_EX, "\033[95m");
    EXPECT_STREQ(Fore::LIGHTCYAN_EX, "\033[96m");
    EXPECT_STREQ(Fore::LIGHTWHITE_EX, "\033[97m");
}

TEST(AnsiTest, BackAttributes) {
    EXPECT_STREQ(Back::BLACK, "\033[40m");
    EXPECT_STREQ(Back::RED, "\033[41m");
    EXPECT_STREQ(Back::GREEN, "\033[42m");
    EXPECT_STREQ(Back::YELLOW, "\033[43m");
    EXPECT_STREQ(Back::BLUE, "\033[44m");
    EXPECT_STREQ(Back::MAGENTA, "\033[45m");
    EXPECT_STREQ(Back::CYAN, "\033[46m");
    EXPECT_STREQ(Back::WHITE, "\033[47m");
    EXPECT_STREQ(Back::RESET, "\033[49m");
    EXPECT_STREQ(Back::LIGHTBLACK_EX, "\033[100m");
    EXPECT_STREQ(Back::LIGHTRED_EX, "\033[101m");
    EXPECT_STREQ(Back::LIGHTGREEN_EX, "\033[102m");
    EXPECT_STREQ(Back::LIGHTYELLOW_EX, "\033[103m");
    EXPECT_STREQ(Back::LIGHTBLUE_EX, "\033[104m");
    EXPECT_STREQ(Back::LIGHTMAGENTA_EX, "\033[105m");
    EXPECT_STREQ(Back::LIGHTCYAN_EX, "\033[106m");
    EXPECT_STREQ(Back::LIGHTWHITE_EX, "\033[107m");
}

TEST(AnsiTest, StyleAttributes) {
    EXPECT_STREQ(Style::DIM, "\033[2m");
    EXPECT_STREQ(Style::NORMAL, "\033[22m");
    EXPECT_STREQ(Style::BRIGHT, "\033[1m");
}