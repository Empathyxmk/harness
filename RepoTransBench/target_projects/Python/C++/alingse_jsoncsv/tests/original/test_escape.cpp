#include <gtest/gtest.h>
#include "jsoncsv/utils.h"
#include <vector>
#include <string>

TEST(TestEscape, All) {
    std::vector<std::string> path{"A", "B", "..", "\\.\\ww"};
    std::vector<char> seps = {'A','B','.','w'};
    for(char sep : seps) {
        std::string key = encode_safe_key(path, sep);
        auto _path = decode_safe_key(key, sep);
        EXPECT_EQ(path, _path);
    }
}

TEST(TestEscape, Encode) {
    std::vector<std::string> path{"A", "B", "C", "www.xxx.com"};
    char sep = '.';
    std::string key = encode_safe_key(path, sep);
    EXPECT_EQ(key, "A\\.B\\.C\\.www.xxx.com");
}

TEST(TestEscape, Decode) {
    std::string key = "A\\.B\\.C\\.www.xxx.com";
    char sep = '.';
    auto path = decode_safe_key(key, sep);
    ASSERT_EQ(path.size(), 4);
    EXPECT_EQ(path[0], "A");
    EXPECT_EQ(path[1], "B");
    EXPECT_EQ(path[2], "C");
    EXPECT_EQ(path[3], "www.xxx.com");
}