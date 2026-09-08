#include <gtest/gtest.h>
#include "pyzbar/pyzbar.h"

TEST(ZBarSymbolPublic, EnumValues) {
    EXPECT_TRUE(has_ZBarSymbol_CODE39());
    EXPECT_TRUE(is_ZBarSymbol_CODE39_int());
}

TEST(ZBarSymbolPublic, AllSymbolsIncludesSymbol) {
    EXPECT_TRUE(ZBarSymbol_ALL_includes_CODE93());
}