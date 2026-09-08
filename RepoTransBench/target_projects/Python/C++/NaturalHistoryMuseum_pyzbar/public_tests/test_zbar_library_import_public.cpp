#include <gtest/gtest.h>
#include "pyzbar/zbar_library.h"
#include <string>

TEST(ZBarLibraryImportPublic, Importable) {
    std::string file = zbar_library_get_file();
    EXPECT_FALSE(file.empty());
    std::string name = zbar_library_get_name();
    EXPECT_FALSE(name.empty());
}