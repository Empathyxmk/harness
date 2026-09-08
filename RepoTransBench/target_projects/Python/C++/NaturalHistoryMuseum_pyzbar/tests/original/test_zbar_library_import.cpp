#include <gtest/gtest.h>
#include "pyzbar/zbar_library.h"
#include <string>

TEST(ZBarLibraryImport, Importable) {
    std::string file = zbar_library_get_file();
    EXPECT_FALSE(file.empty());
}