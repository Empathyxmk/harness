#include <gtest/gtest.h>
#include "pyzbar/pyzbar_error.h"
#include <stdexcept>
#include <string>

// Assert that PyZbarError derives from std::exception in C++
TEST(PyzbarError, IsExceptionType) {
    EXPECT_TRUE(is_pyzbar_error_a_std_exception());
}

TEST(PyzbarError, RaiseAndStr) {
    try {
        throw PyZbarError("fail");
    } catch (const PyZbarError& e) {
        EXPECT_EQ(std::string(e.what()), "fail");
    }
}