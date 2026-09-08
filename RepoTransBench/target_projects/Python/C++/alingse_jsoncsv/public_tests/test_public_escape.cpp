#include <gtest/gtest.h>
#include "jsoncsv/utils.h"
#include <vector>
#include <string>

TEST(TestPublicEscape, All) {
    std::vector<std::string> path{"A1", "B1", "..2", "\\.\\oo"};
    std::vector<char> seps = {'R','E','P'};
    for(char sep : seps){
        std::string key = encode_safe_key(path, sep);
        auto _path = decode_safe_key(key, sep);
        EXPECT_EQ(path, _path);
    }
}

TEST(TestPublicEscape, Encode) {
    std::vector<std::string> path{"D", "E", "F", "my.site.com"};
    char sep = '.';
    std::string key = encode_safe_key(path, sep);
    EXPECT_EQ(key, "D\\.E\\.F\\.my.site.com");
}

TEST(TestPublicEscape, Decode) {
    std::string key = "X\\.Y\\.Z\\.abc.def.com";
    char sep = '.';
    auto path = decode_safe_key(key, sep);
    ASSERT_EQ(path.size(), 4);
    EXPECT_EQ(path[0], "X");
    EXPECT_EQ(path[1], "Y");
    EXPECT_EQ(path[2], "Z");
    EXPECT_EQ(path[3], "abc.def.com");
}