#include <gtest/gtest.h>
#include "pyzbar/zbar_library.h"
#include <string>
#include <vector>

class ZBarLibraryPublic : public ::testing::Test {};

TEST_F(ZBarLibraryPublic, LibFound) {
    std::string libname = zbar_library_load_public().first;
    EXPECT_FALSE(libname.empty());
    EXPECT_TRUE((libname.find(".so") != std::string::npos)
                || (libname.find(".dll") != std::string::npos)
                || (libname.find(".dylib") != std::string::npos));
}

TEST_F(ZBarLibraryPublic, SearchPathsIncludeLibrary) {
    auto results = zbar_library_search_paths_public();
    bool found = false;
    for(const auto& path : results){
        if(path.find("zbar") != std::string::npos) { found = true; break; }
    }
    EXPECT_TRUE(found);
}