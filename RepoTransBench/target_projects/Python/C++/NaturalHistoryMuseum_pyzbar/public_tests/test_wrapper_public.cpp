#include <gtest/gtest.h>
#include "pyzbar/wrapper.h"
#include <string>

TEST(WrapperPublic, GetSymbolName) {
    std::string name = get_symbol_name(13);
    EXPECT_NE(name.find("PDF417"), std::string::npos);
}

TEST(WrapperPublic, GetSymbolNameInvalid) {
    std::string name = get_symbol_name(1000);
    EXPECT_EQ(name, "UNKNOWN");
}