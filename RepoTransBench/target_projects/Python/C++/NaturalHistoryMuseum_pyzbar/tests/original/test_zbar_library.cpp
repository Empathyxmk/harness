#include <gtest/gtest.h>
#include "pyzbar/zbar_library.h"
#include <stdexcept>
#include <string>
#include <vector>

// Simulate/mock zbar library loading. Mocks are not as easy in C++, so provide stub functions for checking the logic.

TEST(ZBarLibrary, LoadNonWindowsFound) {
    auto res = zbar_library_load_simulated("Not windows", true);
    EXPECT_EQ(res.first, "zbar-so-path");
    EXPECT_TRUE(res.second.empty());
}

TEST(ZBarLibrary, LoadNonWindowsNotFound) {
    EXPECT_THROW(zbar_library_load_simulated("Not windows", false), std::runtime_error);
}

TEST(ZBarLibrary, LoadWindowsFound) {
    auto res = zbar_library_load_simulated("Windows", true);
    EXPECT_EQ(res.first, "zbar-dll-path");
    EXPECT_EQ(res.second.size(), 1);
}

TEST(ZBarLibrary, LoadWindowsSecondAttempt) {
    auto res = zbar_library_load_simulated_second_attempt("Windows");
    EXPECT_EQ(res.first, "zbar-dll-path-2");
    EXPECT_EQ(res.second.size(), 1);
}

TEST(ZBarLibrary, LoadWindowsNotFound) {
    EXPECT_THROW(zbar_library_load_simulated("Windows", false), std::runtime_error);
}

TEST(ZBarLibraryWin, Bitness32) {
    auto fnames = windows_fnames_simulated(32);
    EXPECT_EQ(fnames.first, "libzbar-32.dll");
    ASSERT_EQ(fnames.second.size(), 1);
    EXPECT_EQ(fnames.second[0], "libiconv-2.dll");
}

TEST(ZBarLibraryWin, Bitness64) {
    auto fnames = windows_fnames_simulated(64);
    EXPECT_EQ(fnames.first, "libzbar-64.dll");
    ASSERT_EQ(fnames.second.size(), 1);
    EXPECT_EQ(fnames.second[0], "libiconv.dll");
}