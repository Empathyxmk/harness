#include <gtest/gtest.h>
#include "pyzbar/pyzbar.h"
#include <string>

TEST(Init, VersionExists) {
    // Equivalent of: assert hasattr(pyzbar, '__version__'); isinstance(__version__, str)
    EXPECT_FALSE(get_pyzbar_version().empty());
    EXPECT_TRUE(typeid(get_pyzbar_version()) == typeid(std::string));
}