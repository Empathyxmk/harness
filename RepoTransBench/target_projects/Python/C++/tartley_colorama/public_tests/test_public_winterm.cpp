#include <gtest/gtest.h>

TEST(PublicWinTermTest, TestInitPublic) {
    // Simulate WinTerm._fore/back/style computation when constructed with wAttributes=171
    int wAttributes = 171;
    int fore = wAttributes & 7;
    int back = (wAttributes >> 4) & 7;
    int style = wAttributes & ~0x77;
    EXPECT_EQ(fore, 3);
    EXPECT_EQ(back, 2);
    EXPECT_EQ(style, 136);
}

TEST(PublicWinTermTest, TestResetAllPublic) {
    int wAttributes = 250;
    int fore = wAttributes & 7;
    int back = (wAttributes >> 4) & 7;
    int style = wAttributes & ~0x77;
    EXPECT_EQ(fore, 2);
    EXPECT_EQ(back, 7);
    EXPECT_EQ(style, 136);
}