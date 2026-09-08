#include <gtest/gtest.h>
#include <string>
#include "drawille.h"

TEST(PublicSpeedTest, PublicCanvasSpeed) {
    Canvas canvas;
    for (int y = 0; y < 80; y += 2) {
        canvas.set(15, y);
    }
    std::string buf = canvas.frame();
    // Buffer should not be empty, should contain a braille char
    bool has_braille = false;
    for (char c : buf) {
        if ((unsigned char)c >= 0xE2) { // UTF-8 start for braille
            has_braille = true;
            break;
        }
    }
    EXPECT_TRUE(!buf.empty());

    canvas.clear();
    std::string buf2 = canvas.frame();
    bool has_braille2 = false;
    for (char c : buf2) {
        if ((unsigned char)c >= 0xE2) {
            has_braille2 = true; break;
        }
    }
    EXPECT_TRUE(buf2.empty());
}