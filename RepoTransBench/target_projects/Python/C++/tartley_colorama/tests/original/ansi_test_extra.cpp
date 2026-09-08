#include <gtest/gtest.h>
#include "colorama/ansi.h"

using namespace colorama;

TEST(AnsiTestExtra, CodeToCharsAndClearScreen) {
    EXPECT_EQ(code_to_chars("1"), "\033[1m");
    EXPECT_EQ(code_to_chars("1;31"), "\033[1;31m");
}

TEST(AnsiTestExtra, ClearLineAndScreenMethods) {
    EXPECT_TRUE(clear_line(2).size() > 0);
    EXPECT_TRUE(clear_screen(1).size() > 0);
    EXPECT_TRUE(clear_line().size() > 0);
    EXPECT_TRUE(clear_screen().size() > 0);
}

TEST(AnsiTestExtra, CursorMethods) {
    EXPECT_NE(Cursor::UP(1).find("\033[1A"), std::string::npos);
    EXPECT_NE(Cursor::DOWN(1).find("\033[1B"), std::string::npos);
    EXPECT_NE(Cursor::BACK(1).find("\033[1D"), std::string::npos);
    EXPECT_NE(Cursor::FORWARD(1).find("\033[1C"), std::string::npos);
    EXPECT_TRUE(Cursor::POS(2, 3).size() > 0);
}

TEST(AnsiTestExtra, SetTitleMethod) {
    EXPECT_NE(set_title("abc").find("\033]0;"), std::string::npos);
}

TEST(AnsiTestExtra, ForeStyleClassRepr) {
    // Just check typeid().name() is non-empty for class types (C++ analog to repr)
    EXPECT_TRUE(std::string(typeid(Fore).name()).size() > 0);
    EXPECT_TRUE(std::string(typeid(Back).name()).size() > 0);
    EXPECT_TRUE(std::string(typeid(Style).name()).size() > 0);
    EXPECT_TRUE(std::string(typeid(Cursor).name()).size() > 0);
}