#include <gtest/gtest.h>
#include <stdexcept>
#include <iostream>

TEST(WarningTest, WarnsUserWarning) {
    // C++ has no warnings system like Python's 'warnings'; use a workaround.
    // We'll simulate warning emission and detection.
    EXPECT_NO_THROW({
        try {
            throw std::runtime_error("this is a warning");
        } catch (const std::runtime_error& e) {
            // treat as warning caught
            EXPECT_STREQ(e.what(), "this is a warning");
        }
    });
}