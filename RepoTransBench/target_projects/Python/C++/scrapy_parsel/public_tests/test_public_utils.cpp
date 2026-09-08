#include <gtest/gtest.h>
#include "utils.h"

TEST(PublicUtils, ToUnicodeIntInput) {
    EXPECT_EQ(to_unicode(6789), "6789");
}

TEST(PublicUtils, ToUnicodeByteInput) {
    std::vector<uint8_t> bytes = {'N', 'e', 'w', 'T', 'e', 's', 't'};
    EXPECT_EQ(to_unicode(bytes), "NewTest");
}

TEST(PublicUtils, ToUnicodeStrInput) {
    EXPECT_EQ(to_unicode("UnicodeStringTest"), "UnicodeStringTest");
}

TEST(PublicUtils, ToUnicodeError) {
    class A {};
    EXPECT_THROW({
        throw std::invalid_argument("TypeError on to_unicode");
    }, std::invalid_argument);
}